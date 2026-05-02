from fastapi import APIRouter, Request

from src.models.base import HealthResponse

router = APIRouter()

@router.get("/v1/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    return HealthResponse(
        status="ok", 
        version=request.app.state.version, 
        env=request.app.state.env)

@router.get("/v1/ready", response_model=HealthResponse)
async def ready(request: Request) -> HealthResponse:
    return HealthResponse(
        status="ok", 
        version=request.app.state.version, 
        env=request.app.state.env)