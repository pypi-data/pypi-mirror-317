import traceback
from typing import Literal

import celery
from django.conf import settings
from django.utils import timezone
from django.views import View

from .apis import post_or_put_celery_log
from .helpers import LogSettings, format_django_traceback, get_log_dict

settings: LogSettings = getattr(settings, "LOG_SETTINGS", None)


class TaskLogger(celery.Task):

    def add_log(
        self,
        level: Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        message: str,
    ):
        """
        Add log to the log object
        """
        if not hasattr(self.request, "add_log") and callable(self.request.add_log):
            raise AttributeError(
                "Request object does not have add_log method. Add LogMiddleware to the middleware list"
            )

        self.request.add_log(level, message)

    def __call__(self, *args, **kwargs):
        if not settings.enabled:
            return super().__call__(*args, **kwargs)
        log = {
            "task_id": self.request.id,
            "task_name": self.name,
            "periodic_task_name": (
                self.request.periodic_task_name[:255]
                if hasattr(self.request, "periodic_task_name")
                else None
            ),
            "args": args or None,
            "kwargs": kwargs or None,
            "context": self.request.__dict__,
            "started_at": timezone.now().timestamp(),
        }
        post_or_put_celery_log(log, "POST")
        error = None
        updated_log = {"task_id": self.request.id}
        to_return = None

        def _add_log(level, message):

            log = get_log_dict(level, message)

            if not log:
                return

            if not updated_log.get("logs"):
                updated_log["logs"] = []

            updated_log["logs"].append(log)

        setattr(self.request, "add_log", _add_log)

        try:
            to_return = super().__call__(*args, **kwargs)
        except Exception as e:
            updated_log["error"] = {
                "error": str(e),
                "traceback": traceback.format_exc(),
                "formatted_traceback": format_django_traceback(
                    exc_value=e,
                    exc_tb=e.__traceback__,
                    project_folder=settings.project_folder,
                ),
            }
            error = e
        finally:
            updated_log["ended_at"] = timezone.now().timestamp()
            post_or_put_celery_log(updated_log, "PUT")
            if error:
                raise error
        return to_return


class APILogView(View):
    """
    Extends this class to have code editor suggestions for log settings
    """

    skip_request_body: bool
    skip_request_body_methods: list[str]
    skip_request_headers: bool
    skip_request_headers_methods: list[str]
    skip_response_body: bool
    skip_response_body_methods: list[str]
    priority_log_methods: list[str]

    def add_log(
        self,
        level: Literal["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        message: str,
    ):
        """
        Add log to the log object
        """
        if not hasattr(self.request, "add_log") and callable(self.request.add_log):
            raise AttributeError(
                "Request object does not have add_log method. Add LogMiddleware to the middleware list"
            )

        self.request.add_log(level, message)
