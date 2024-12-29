"""Configuration for python's logging utilties."""

import logging
import os


def create_log_config(
    logger_name: str,
    log_level: str = "INFO",
    max_bytes: int = 1024 * 1024,
) -> dict:
    """Create a new logger configuration that can be passed directly to `logging.config.dictConfig`."""
    uvicorn_log_format = f"%(levelprefix)s [{logger_name}] %(message)s"
    json_log_format = f"%(name)s | %(levelname)s | %(asctime)s | %(message)s"
    date_fmt = "%Y-%m-%dT%H:%M:%S%z"
    """ISO-8601 Timestamp with timezone. 'Trust Me' - https://www.youtube.com/watch?v=9L77QExPmI0&t=185s"""

    conf = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": uvicorn_log_format,
            },
            "json": {
                "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
                "format": json_log_format,
                "datefmt": date_fmt,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "json-lines": {
                "formatter": "json",
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "filename": f"logs/{logger_name}.jsonl",
                "maxBytes": max_bytes,
                "backupCount": 3,
            },
        },
        "loggers": {
            logger_name: {"handlers": ["json-lines", "default"], "level": log_level},
        },
    }

    return conf


def get_logger(logger_name: str) -> logging.Logger:
    """Get a logger configured for a custom named service.

    Returns
    -------
    logging.Logger
        Logger with `logger_name` as a prefix and using uvicorn formatting.

    Examples
    --------
    >>> sqlbuilder_logger = get_logger("sqlbuilder")
    """
    from logging.config import dictConfig

    # If the ./logs directory doesn't exist, then the call to `dictConfig` will fail.
    if not os.path.exists("logs"):
        os.makedirs("logs", exist_ok=True)

    # Configure the logging library with `dictConfig`
    dictConfig(create_log_config(logger_name))
    logger = logging.getLogger(logger_name)
    logger.propagate = False

    return logger


logger = get_logger("jupyter-manager")
