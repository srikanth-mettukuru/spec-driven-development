from pydantic import BaseModel


class APIError(BaseModel):
    detail: str
    code: str
    status_code: int

class HealthResponse(BaseModel):
    status: str
    version: str
    env: str
