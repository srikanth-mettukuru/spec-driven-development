import pytest
from pydantic import ValidationError
from src.models.base import APIError, HealthResponse

def test_APIError_valid_payload():
    instance = APIError(detail="Error occurred", code="ERROR_CODE", status_code=400)
    assert instance.detail == "Error occurred"
    assert instance.code == "ERROR_CODE"
    assert instance.status_code == 400

def test_APIError_missing_required_field():
    with pytest.raises(ValidationError):
        APIError(code="ERROR_CODE", status_code=400)

def test_APIError_invalid_field_type():
    with pytest.raises(ValidationError):
        APIError(detail=["not", "a", "string"], code="ERROR_CODE", status_code=400)

def test_HealthResponse_valid_payload():
    instance = HealthResponse(status="ok", version="1.0.0", env="production")
    assert instance.status == "ok"
    assert instance.version == "1.0.0"
    assert instance.env == "production"

def test_HealthResponse_missing_required_field():
    with pytest.raises(ValidationError):
        HealthResponse(version="1.0.0", env="production")

def test_HealthResponse_invalid_field_type():
    with pytest.raises(ValidationError):
        HealthResponse(status=["not", "a", "string"], version="1.0.0", env="production")
