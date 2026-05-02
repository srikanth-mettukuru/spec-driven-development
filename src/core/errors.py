import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class APIError(BaseModel):
    detail: str
    code: str
    status_code: int

async def handle_validation_error(
        request: Request, 
        exc: RequestValidationError
    ) -> JSONResponse:
    logger.error("Validation error: %s", exc)
    return JSONResponse(
        status_code=422,
        content=APIError(
            detail=str(exc), 
            code="VALIDATION_ERROR", 
            status_code=422
            ).dict()
    )

async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    logger.error("HTTP error: %s", exc)
    return JSONResponse(
        status_code=exc.status_code,
        content=APIError(
            detail=exc.detail, 
            code="HTTP_ERROR", 
            status_code=exc.status_code
            ).dict()
    )

async def handle_generic_exception(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled exception: %s", exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content=APIError(
            detail="An unexpected error occurred", 
            code="INTERNAL_ERROR", 
            status_code=500
            ).dict()
    )

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, handle_validation_error) # type: ignore[arg-type]
    app.add_exception_handler(HTTPException, handle_http_exception) # type: ignore[arg-type]
    app.add_exception_handler(Exception, handle_generic_exception)