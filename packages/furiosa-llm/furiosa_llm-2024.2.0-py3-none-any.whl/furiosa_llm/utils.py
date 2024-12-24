import logging
import sys
from typing import Optional

if sys.version_info >= (3, 10):
    def zip_equal(*iterables):  # fmt: skip
        return zip(*iterables, strict=True)
else:
    from more_itertools import zip_equal  # noqa


_modified_handlers = set()


def get_logger_with_tz(logger: logging.Logger) -> logging.Logger:
    """
    This function is used to add timezone info to logging.Logger's formatter.
    Mind that this function updates in-place, and the ancestor handlers of the logger as well.
    So if called to some logger, it may update the root logger as well.
    """
    global _modified_handlers
    current_logger: Optional[logging.Logger] = logger
    # Traverse up the logger hierarchy to modify all relevant handlers
    while current_logger:
        for handler in current_logger.handlers:
            if handler in _modified_handlers:
                continue
            _modified_handlers.add(handler)
            if handler.formatter:
                if handler.formatter.datefmt:
                    handler.formatter.datefmt += "%z"
                else:
                    handler.formatter.datefmt = logging.Formatter.default_time_format + "%z"
            else:
                handler.setFormatter(
                    logging.Formatter(datefmt=logging.Formatter.default_time_format + "%z")
                )
        if not current_logger.propagate:
            break
        current_logger = current_logger.parent

    return logger
