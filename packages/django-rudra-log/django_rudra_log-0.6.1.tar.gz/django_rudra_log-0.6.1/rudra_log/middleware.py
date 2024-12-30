import os
import traceback

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings
from django.http import HttpRequest
from django.urls import resolve
from django.utils import timezone

from .apis import post_api_log
from .helpers import LogSettings, format_django_traceback, get_log_dict


class LoggingMiddleware:
    async_capable = True
    sync_capable = False

    settings: LogSettings

    method = None
    request_body = None
    headers = None

    skip_request_body = False
    skip_request_body_methods = []
    skip_request_headers = False
    skip_request_headers_methods = []
    skip_response_body = False
    skip_response_body_methods = []
    priority_log_methods = []

    _log = {}

    def __init__(self, get_response):
        self.settings = getattr(settings, "LOG_SETTINGS")
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    def __is_path_excluded__(self, path: str):
        return any(
            path.startswith(excluded_path)
            for excluded_path in self.settings.paths_to_exclude
        )

    @property
    def __can_skip_logging__body(self):
        return self.skip_request_body or self.method in self.skip_request_body_methods

    @property
    def __can_skip_logging__headers(self):
        return (
            self.skip_request_headers
            or self.method in self.skip_request_headers_methods
        )

    @property
    def __can_skip_logging__response_body(self):
        return self.skip_response_body or self.method in self.skip_response_body_methods

    @property
    def __is_api_priority_log__(self):
        return self.method in self.priority_log_methods

    def update_post_response_data(self, request, response):
        # in django request's user is SimpleLazyObject, if we try to access it before response is composed, it will raise an error since it's not yet evaluated and evaluation will make db call in sync mode
        if (
            not hasattr(request.user, "_wrapped")
            or type(request.user._wrapped) != object
        ):  # if user object has no "_wrapped" attribute or it's not an SimpleLazyObject, then it's already evaluated
            # this way we can check if user is SimpleLazyObject, if request.user is evaluated, it will be of some User model type
            self._log["user"] = {
                "id": request.user.id if request.user.is_authenticated else None,
                "email": (
                    request.user.email if request.user.is_authenticated else None
                ),
            }

        self._log["status_code"] = self.settings.get_status_code(response)
        self._log["headers"] = (
            self.settings.clean_header(dict(request.headers))
            if not self.__can_skip_logging__headers
            else None
        )
        content_type = self._log["headers"].get("Content-Type")
        if content_type != "application/json" or self.__can_skip_logging__body:
            self._log["body"] = (
                None  # body can't be accessed after response is composed
            )
        else:
            if self._log["body"] and isinstance(self._log["body"], bytes):
                self._log["body"] = self._log["body"].decode(
                    "utf-8"
                )  # decode bytes to string

        self._log["response"] = (
            response.content.decode("utf-8")
            if not self.__can_skip_logging__response_body
            and response.headers.get("Content-Type") == "application/json"
            else None
        )
        self._log["ended_at"] = timezone.now().timestamp()

    async def __call__(self, request: HttpRequest):
        if self.__is_path_excluded__(request.path) or not self.settings.enabled:
            return await self.get_response(request)

        view, _, _ = resolve(request.path)
        self.skip_request_body = getattr(
            view,
            "view_class",
            None,
        ) and getattr(
            view.view_class,
            "skip_request_body",
            False,
        )
        self.skip_request_body_methods = (
            getattr(
                view,
                "view_class",
                None,
            )
            and getattr(
                view.view_class,
                "skip_request_body_methods",
                None,
            )
            or []
        )
        self.skip_request_headers = getattr(
            view,
            "view_class",
            None,
        ) and getattr(
            view.view_class,
            "skip_request_headers",
            False,
        )
        self.skip_request_headers_methods = (
            getattr(
                view,
                "view_class",
                None,
            )
            and getattr(
                view.view_class,
                "skip_request_headers_methods",
                None,
            )
            or []
        )
        self.skip_response_body = getattr(
            view,
            "view_class",
            None,
        ) and getattr(
            view.view_class,
            "skip_response_body",
            False,
        )
        self.priority_log_methods = (
            getattr(
                view,
                "view_class",
                None,
            )
            and getattr(
                view.view_class,
                "priority_log_methods",
                None,
            )
            or []
        )

        self._log = {
            "path": request.path,
            "query_params": request.GET.dict(),
            "method": request.method,
            "started_at": timezone.now().timestamp(),
        }

        self._log["body"] = request.body

        def _add_log(level, message):

            log = get_log_dict(level, message)

            if not log:
                return

            if not self._log.get("logs"):
                self._log["logs"] = []

            self._log["logs"].append(log)

        setattr(request, "add_log", _add_log)

        response = await self.get_response(request)
        self.update_post_response_data(request, response)
        post_api_log(self._log, self.__is_api_priority_log__)

        return response

    def process_exception(self, request: HttpRequest, e):
        if not self.settings.enabled:
            return None

        response = self.settings.app_exception_handler(
            request, e, traceback.format_exc()
        )
        if not self.settings.can_ignore_exception(e):
            self._log["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "formatted_traceback": format_django_traceback(
                    exc_value=e,
                    exc_tb=e.__traceback__,
                    project_folder=self.settings.project_folder,
                ),
            }
        return response
