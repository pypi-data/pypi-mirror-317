import logging
import logging.config
import sys

LOGGING_LINE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOGGING_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


class LDSILoggingStream:
    """
    A Python stream for use with event logging APIs throughout LDSI (`eprint()`,
    `logger.info()`, etc.). This stream wraps `sys.stderr`, forwarding `write()` and
    `flush()` calls to the stream referred to by `sys.stderr` at the time of the call.
    It also provides capabilities for disabling the stream to silence event logs.
    """

    def __init__(self):
        self._enabled = True

    def write(self, text):
        if self._enabled:
            sys.stderr.write(text)

    def flush(self):
        if self._enabled:
            sys.stderr.flush()

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, value):
        self._enabled = value


LDSI_LOGGING_STREAM = LDSILoggingStream()


def disable_logging():
    """
    Disables the `LDSILoggingStream` used by event logging APIs throughout LDSI
    (`eprint()`, `logger.info()`, etc), silencing all subsequent event logs.
    """
    LDSI_LOGGING_STREAM.enabled = False


def enable_logging():
    """
    Enables the `LDSILoggingStream` used by event logging APIs throughout LDSI
    (`eprint()`, `logger.info()`, etc), emitting all subsequent event logs. This
    reverses the effects of `disable_logging()`.
    """
    LDSI_LOGGING_STREAM.enabled = True


def configure_ldsi_loggers(root_module_name):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "ldsi_formatter": {
                    "format": LOGGING_LINE_FORMAT,
                    "datefmt": LOGGING_DATETIME_FORMAT,
                },
            },
            "handlers": {
                "ldsi_handler": {
                    "formatter": "ldsi_formatter",
                    "class": "logging.StreamHandler",
                    "stream": LDSI_LOGGING_STREAM,
                },
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["ldsi_handler"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
    )
