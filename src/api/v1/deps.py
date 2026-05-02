import uuid

from fastapi import Header


def get_trace_id(x_trace_id: str = Header(default=None)) -> str:
    return x_trace_id or str(uuid.uuid4())
