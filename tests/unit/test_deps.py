import uuid
from src.api.v1.deps import get_trace_id

def test_get_trace_id_returns_uuid_when_header_absent():
    result = get_trace_id(x_trace_id=None)
    uuid.UUID(result)  # This will raise ValueError if the result is not a valid UUID

def test_get_trace_id_returns_header_value_when_present():
    result = get_trace_id(x_trace_id="test-trace-id")
    assert result == "test-trace-id"
