import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from src.core.errors import register_exception_handlers
from src.api.v1.health import router as health_router

class SampleBody(BaseModel):
    name: str

@pytest.fixture
def client():
    app = FastAPI()
    register_exception_handlers(app)
    app.state.version = "0.1.0"
    app.state.env = "test"
    app.include_router(health_router)

    @app.get("/trigger-500")
    async def trigger_500():
        raise Exception("Unexpected error")

    @app.post("/trigger-validation")
    async def trigger_validation(body: SampleBody):
        return body

    return TestClient(app, raise_server_exceptions=False)
