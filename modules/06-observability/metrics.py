"""Module 06: structured logging + metrics emission.

Both write newline-delimited JSON to files in this directory, so they can
be queried with jq, loaded into pandas, or shipped to a real log/metrics
backend without changing the call sites in your pipeline code.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOG_FILE = Path(__file__).resolve().parent / "logs.jsonl"
METRICS_FILE = Path(__file__).resolve().parent / "metrics.jsonl"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit_log(level: str, message: str, **fields: Any) -> None:
    record = {"timestamp": _now_iso(), "level": level, "message": message, **fields}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record))
        f.write("\n")


def emit_metric(name: str, value: float, **tags: Any) -> None:
    record = {"timestamp": _now_iso(), "metric": name, "value": value, **tags}
    with open(METRICS_FILE, "a") as f:
        f.write(json.dumps(record))
        f.write("\n")


class timed_metric:
    """Context manager that emits a duration_seconds metric on exit.

    Usage:
        with timed_metric("load_duration_seconds", pipeline="course_dag"):
            load_landing_file_to_warehouse(date)
    """

    def __init__(self, name: str, **tags: Any):
        self.name = name
        self.tags = tags
        self._start = None

    def __enter__(self):
        self._start = datetime.now(timezone.utc)
        return self

    def __exit__(self, exc_type, exc, tb):
        duration = (datetime.now(timezone.utc) - self._start).total_seconds()
        emit_metric(self.name, duration, **self.tags)
        return False
