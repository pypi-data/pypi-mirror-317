import inspect
import os
import sys
import threading
import time
import traceback

# import logging
from logging import _nameToLevel, root
from typing import Callable

from asgiref.sync import iscoroutinefunction, markcoroutinefunction
from django.conf import settings
from django.http import HttpRequest, HttpResponse


class LogSettings:
    def __init__(
        self,
        url: str,
        env_key: str,
        enabled: bool,
        app_exception_handler: Callable[[HttpRequest, Exception, str], HttpResponse],
        can_ignore_exception: Callable[[Exception], bool] = lambda x: False,
        paths_to_exclude: list[str] = [],
        clean_header: Callable[[dict], dict] = lambda x: x,
        get_status_code: Callable[[HttpResponse], int] = lambda x: x.status_code,
        use_thread_pool: bool = True,
        thread_pool_size: int = 24,
        project_folder: str = "/backend/",
    ):
        self.url = url
        self.env_key = env_key
        self.enabled = enabled
        self.app_exception_handler = app_exception_handler
        self.can_ignore_exception = can_ignore_exception
        self.paths_to_exclude = paths_to_exclude
        self.clean_header = clean_header
        self.get_status_code = get_status_code
        self.use_thread_pool = use_thread_pool
        self.thread_pool_size = thread_pool_size
        self.project_folder = project_folder


class MiddlewareWrapper:
    """
    This class is a wrapper around the middleware class, it helps to catch exceptions raised by custom middleware and handle them by the app_exception_handler.
    """

    settings: LogSettings
    async_capable = True
    sync_capable = False

    def __init__(self, get_response):
        self.settings = getattr(settings, "LOG_SETTINGS")
        self.get_response = get_response
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    async def process(self, request):
        raise NotImplementedError

    async def __call__(self, request):
        try:
            return await self.process(request)
        except Exception as e:
            if not self.settings.enabled or not self.settings.can_ignore_exception(e):
                raise e
            return self.settings.app_exception_handler(
                request, e, traceback.format_exc()
            )


def _format_django_traceback(exc_value, exc_tb, project_folder="/backend/", prefix=""):
    """Format traceback to include both Django and project-specific code with highlights."""
    output = []
    tb = exc_tb  # Start with the traceback object

    while tb:
        frame = tb.tb_frame  # Get the frame object
        lineno = tb.tb_lineno  # Line number where the exception occurred
        filename = frame.f_code.co_filename  # File name of the frame
        funcname = frame.f_code.co_name  # Function name of the frame

        # Check if the frame belongs to the project
        is_project_code = project_folder in filename

        if not is_project_code:
            # move to the next traceback object
            tb = tb.tb_next
            continue

        output.append(
            f"{prefix}File: {filename}, Line: {lineno}, Function: {funcname}\n"
        )
        output.append(
            prefix + filename.replace(project_folder, "") + ":" + str(lineno) + "\n"
        )

        try:
            with open(filename, "r") as f:
                lines = f.readlines()
                context_lines = lines[
                    max(0, lineno - 4) : lineno + 3
                ]  # 3-4 lines around the error
                for i, line in enumerate(context_lines, start=max(0, lineno - 4)):
                    suffix = ""
                    if i + 1 == lineno:
                        suffix = " <--- This caused the exception"

                    if line.startswith("    "):
                        line = line[4:]  # Removing first indentation

                    if line[-1] == "\n":
                        line = line[:-1] + suffix + "\n"
                    else:
                        line = line + suffix
                    output.append(f"{prefix}{i + 1}: {line}")
        except Exception as e:
            output.append(f"{prefix}Could not retrieve surrounding code: {e}\n")

        # Add local variables
        local_vars = frame.f_locals
        if local_vars:
            output.append(f"\n{prefix}Local Variables:\n")
            for var, value in local_vars.items():
                # check if the value are not primitive types
                if not isinstance(value, (int, float, str, bool, list, dict)):
                    continue
                output.append(f"{prefix}     {var}: {value}\n")

        # add a line break
        output.append(
            "\n"
            + prefix
            + "-" * 10
            + f"End of project file {filename}"
            + "-" * 10
            + "\n\n"
        )

        tb = tb.tb_next  # Move to the next traceback object

    if exc_value.__cause__:
        output.append(
            "\nThe above exception happened while handling the following exception:\n"
        )
        cause_tb = exc_value.__cause__.__traceback__
        output.append(
            _format_django_traceback(
                type(exc_value.__cause__),
                cause_tb,
                project_folder,
                prefix + "  ",
            )
        )

    return "".join(output)


def format_django_traceback(exc_value, exc_tb, project_folder="/backend/"):
    try:
        return _format_django_traceback(exc_value, exc_tb, project_folder)
    except Exception as e:
        return f"Error while formatting traceback: \n\nError: {e}\n\ntraceback{traceback.format_exc()}"


def get_log_dict(level: str, message: str):
    current_level = root.getEffectiveLevel()
    level_int = _nameToLevel[level]

    # skip logs with level lower than current level
    if level_int < current_level:
        return None

    frame = (
        inspect.currentframe().f_back.f_back.f_back
    )  # go back 3 frames to get the actual caller
    code = frame.f_code
    filename = code.co_filename
    lineno = frame.f_lineno
    func_name = frame.f_code.co_name

    # Get the time information
    created_time = time.time()
    asctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
    msecs = int((created_time - int(created_time)) * 1000)
    relative_created = int(created_time * 1000)  # Relative time in milliseconds
    thread_id = threading.get_ident()
    thread_name = threading.current_thread().name
    process_id = os.getpid()
    processName = "MainProcess"
    mp = sys.modules.get("multiprocessing")
    if mp is not None:
        # Errors may occur if multiprocessing has not finished loading
        # yet - e.g. if a custom import hook causes third-party code
        # to run when multiprocessing calls import. See issue 8200
        # for an example
        try:
            processName = mp.current_process().name
        except Exception:  # pragma: no cover
            pass

    return {
        "levelname": level,
        "pathname": filename,  # Full pathname of the source file
        "filename": os.path.basename(filename),  # Filename portion of the pathname
        "module": filename.split("/")[-1].split(".")[0],  # Module name from filename
        "lineno": lineno,  # Line number where log is generated
        "funcName": func_name,  # Function name
        "created": created_time,  # Time when the LogRecord was created (in seconds)
        "asctime": asctime,  # Textual time when the LogRecord was created
        "msecs": msecs,  # Millisecond portion of the creation time
        "relativeCreated": relative_created,  # Relative time in milliseconds since app start
        "thread": thread_id,
        "threadName": thread_name,
        "process": process_id,
        "processName": processName,
        "message": message,
    }
