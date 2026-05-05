import logging
import sys
import uuid
from contextvars import ContextVar

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")


class CorrelationIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.correlation_id = correlation_id_var.get("")  # type: ignore[attr-defined]
        return True


def setup_logging() -> logging.Logger:
    logger = logging.getLogger("cs_platform")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '{"timestamp":"%(asctime)s","level":"%(levelname)s","correlation_id":"%(correlation_id)s","module":"%(name)s","message":"%(message)s"}'
    )
    handler.setFormatter(formatter)
    handler.addFilter(CorrelationIdFilter())

    logger.addHandler(handler)
    return logger


def generate_correlation_id() -> str:
    return uuid.uuid4().hex[:16]


logger = setup_logging()
