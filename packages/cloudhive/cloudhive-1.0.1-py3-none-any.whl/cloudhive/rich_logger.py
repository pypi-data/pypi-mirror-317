from rich.logging import RichHandler
import logging


def logger(level=None, log_format=None, dateformat=None) ->logging:
    if not level:
        level = "info"

    if not log_format:
        log_format = "%(message)s"

    if not dateformat:
        dateformat = "[%X]"

    logging.basicConfig(
        level=level.upper(),
        format=log_format,
        datefmt=dateformat,
        handlers=[RichHandler(rich_tracebacks=True, enable_link_path=True)]
    )
    return logging.getLogger("rich")
