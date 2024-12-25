"""Class to handle logging."""

from __future__ import annotations

from collections.abc import Mapping
import logging
import logging.handlers
import os
import queue
import re
import sys
import threading
import traceback
from typing import Any, cast

from pconn import __path__ as GLL_PATH
from pconn.const import DATA_LOGGING, FORMAT_DATETIME
from pconn.core import PConn

DOMAIN = "logger"
_LOGGER = logging.getLogger(__name__)


def _figure_out_source(
    record: logging.LogRecord, call_stack: list[tuple[str, int]], paths_re: re.Pattern
) -> tuple[str, int]:
    # If a stack trace exists, extract file names from the entire call stack.
    # The other case is when a regular "log" is made (without an attached
    # exception). In that case, just use the file where the log was made from.
    if record.exc_info:
        stack = [(x[0], x[1]) for x in traceback.extract_tb(record.exc_info[2])]
    else:
        index = -1
        for i, frame in enumerate(call_stack):
            if frame[0] == record.pathname:
                index = i
                break
        if index == -1:
            # For some reason we couldn't find pathname in the stack.
            stack = [(record.pathname, record.lineno)]
        else:
            stack = call_stack[0 : index + 1]

    # Iterate through the stack call (in reverse) and find the last call from
    # a file in Home Assistant. Try to figure out where error happened.
    for pathname in reversed(stack):
        # Try to match with a file within Home Assistant
        if match := paths_re.match(pathname[0]):
            return (cast(str, match.group(1)), pathname[1])
    # Ok, we don't know what this is
    return (record.pathname, record.lineno)


class LogEntry:
    """Store HA log entries."""

    def __init__(self, record: logging.LogRecord, source: tuple[str, int]) -> None:
        """Initialize a log entry."""
        self.timestamp = record.created
        self.name = record.name
        self.level = record.levelname
        self.message = record.getMessage()
        self.exception = ""
        self.root_cause = None
        if record.exc_info:
            self.exception = "".join(traceback.format_exception(*record.exc_info))
            _, _, tb = record.exc_info  # pylint: disable=invalid-name
            # Last line of traceback contains the root cause of the exception
            if traceback.extract_tb(tb):
                self.root_cause = str(traceback.extract_tb(tb)[-1])
        self.source = source
        self.count = 1

    def to_dict(self) -> dict[str, Any]:
        """Convert object into dict to maintain backward compatibility."""
        return {
            "name": self.name,
            "message": [self.message],
            "level": self.level,
            "source": self.source,
            "timestamp": self.timestamp,
            "exception": self.exception,
            "count": self.count,
        }


class LogErrorHandler(logging.Handler):
    """Log handler for error messages."""

    def __init__(self, paths_re: re.Pattern) -> None:
        """Initialize a new LogErrorHandler."""
        super().__init__()
        self.records: list[dict[str, Any]] = []
        self.paths_re = paths_re

    def emit(self, record: logging.LogRecord) -> None:
        """Save error and warning logs.

        Everything logged with error or warning is saved in local buffer. A
        default upper limit is set to 50 (older entries are discarded) but can
        be changed if needed.
        """
        stack = []
        if not record.exc_info:
            stack = [(f[0], f[1]) for f in traceback.extract_stack()]
        entry = LogEntry(record, _figure_out_source(record, stack, self.paths_re))
        self.records.append(entry.to_dict())


def async_setup_logger(pconn: PConn) -> bool:
    """Set up the logger component."""
    fmt = "%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s"
    try:
        # pylint: disable-next=import-outside-toplevel
        from colorlog import ColoredFormatter

        # basicConfig must be called after importing colorlog in order to
        # ensure that the handlers it sets up wraps the correct streams.
        logging.basicConfig(level=logging.INFO)

        colorfmt = f"%(log_color)s{fmt}%(reset)s"
        logging.getLogger().handlers[0].setFormatter(
            ColoredFormatter(
                colorfmt,
                datefmt=FORMAT_DATETIME,
                reset=True,
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red",
                },
            )
        )
    except ImportError:
        pass
    logging.basicConfig(format=fmt, datefmt=FORMAT_DATETIME, level=logging.INFO)
    logging.captureWarnings(True)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    sys.excepthook = lambda *args: logging.getLogger(None).exception(
        "Uncaught exception", exc_info=args
    )
    threading.excepthook = lambda args: logging.getLogger(None).exception(
        "Uncaught thread exception",
        exc_info=(  # type: ignore[arg-type]
            args.exc_type,
            args.exc_value,
            args.exc_traceback,
        ),
    )
    err_log_path = pconn.config.path("platform-connectors.log")
    gll_path: str = GLL_PATH[0]
    paths_re = re.compile(
        r"(?:{})/(.*)".format(
            "|".join([re.escape(x) for x in (gll_path, str(pconn.config.config_dir))])
        )
    )
    err_path_exists = os.path.isfile(err_log_path)
    if (err_path_exists and os.access(err_log_path, os.W_OK)) or (
        not err_path_exists and os.access(pconn.config.config_dir, os.W_OK)
    ):
        err_handler = logging.handlers.TimedRotatingFileHandler(
            err_log_path, when="midnight", backupCount=1
        )
        err_handler.setLevel(logging.WARN)
        err_handler.setFormatter(logging.Formatter(fmt, datefmt=FORMAT_DATETIME))
        logger = logging.getLogger("")
        logger.addHandler(err_handler)
        logger.setLevel(logging.WARNING)
        pconn.data[DATA_LOGGING] = err_log_path

    else:
        _LOGGER.error("Unable to set up error log %s (access denied)", err_log_path)
    async_activate_log_queue_handler()
    handler = LogErrorHandler(paths_re)
    handler.setLevel(logging.WARNING)
    logging.root.addHandler(handler)
    pconn.data[DOMAIN] = handler
    return True


class QueueHandler(logging.handlers.QueueHandler):
    """Process the log in another thread."""

    listener: logging.handlers.QueueListener | None = None

    def handle(self, record: logging.LogRecord) -> Any:
        """Conditionally emit the specified logging record."""
        return_value = self.filter(record)
        if return_value:
            self.emit(record)
        return return_value

    def close(self) -> None:
        """Tidy up any resources used by the handler.

        This adds shutdown of the QueueListener
        """
        super().close()
        if not self.listener:
            return
        self.listener.stop()
        self.listener = None


def async_activate_log_queue_handler() -> None:
    """Migrate the existing log handlers to use the queue.

    This allows us to avoid blocking I/O and formatting messages
    in the event loop as log messages are written in another thread.
    """
    simple_queue: queue.SimpleQueue[logging.Handler] = queue.SimpleQueue()
    queue_handler = QueueHandler(simple_queue)
    logging.root.addHandler(queue_handler)

    migrated_handlers: list[logging.Handler] = []
    for handler in logging.root.handlers[:]:
        if handler is queue_handler:
            continue
        logging.root.removeHandler(handler)
        migrated_handlers.append(handler)

    listener = logging.handlers.QueueListener(simple_queue, *migrated_handlers)
    queue_handler.listener = listener

    listener.start()


def set_log_levels(log_points: Mapping[str, str]) -> None:
    """Set the specified log levels."""
    for key, value in log_points.items():
        if key == "pconn":
            logging.getLogger("").setLevel(value)
        else:
            logging.getLogger(key).setLevel(value)
