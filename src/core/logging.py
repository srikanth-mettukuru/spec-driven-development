import json
import logging
from datetime import datetime


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "trace_id": getattr(record, "trace_id", "none"),
        }
        return json.dumps(log_record)

class TraceIdFilter(logging.Filter):
    def __init__(self, name: str = "") -> None:
        super().__init__(name)
        self.trace_id: str | None = None

    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = self.trace_id or "none"
        return True

def configure_logging(log_level: str) -> None:
    logging.basicConfig(level=log_level)
    logger = logging.getLogger()
    logger.handlers.clear()
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    logger.addFilter(TraceIdFilter())
