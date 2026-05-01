# Spec: foundation — reusable core infrastructure
 
## Meta
- Feature   : Reusable core infrastructure — logging, errors, models, deps, health
- Endpoint  : n/a — no API endpoints, infrastructure only
- Author    : backend team
- Status    : ready for codegen
- Note      : Generated files belong in the shared template repo.
              Copy them unchanged into every new FastAPI AI project.

## Context files
# No context files — this is the base template layer.
# Everything is generated from scratch based on skills.md alone.
 
## Summary
Generate the five core infrastructure files that are identical across
every FastAPI AI application. These files contain zero project-specific
logic — they are pure reusable plumbing. Once generated and reviewed,
they are committed to the shared template repo and copied unchanged
into every new project.
 
## What to generate
 
### src/core/logging.py
Structured JSON logging using Python stdlib logging with a custom
JSON formatter. Designed to be called once at app startup.
 
Requirements:
- JSONFormatter class — formats every log record as a single JSON line
- Each JSON log line must include:
    timestamp  : ISO 8601 datetime string
    level      : log level name (INFO, ERROR etc)
    message    : the log message
    module     : the calling module name
    trace_id   : value from a logging.Filter if present, else "none"
- TraceIdFilter class — injects trace_id into every log record.
  trace_id is stored on the filter instance and updated per-request
  via a context variable or direct assignment.
- configure_logging(log_level: str) -> None
  Configures the root logger with JSONFormatter and the given level.
  Safe to call multiple times — idempotent.
- Use logging.getLogger(__name__) in all application code —
  never a global logger variable.

### src/core/errors.py
Global FastAPI exception handlers. Catches all unhandled exceptions
and returns structured APIError responses. Raw error messages and
tracebacks never reach the client.
 
Requirements:
- handle_validation_error(request, exc) -> JSONResponse
  Catches RequestValidationError → returns 422 with APIError shape
  detail: first validation error message
  code: "VALIDATION_ERROR"
- handle_http_exception(request, exc) -> JSONResponse
  Catches HTTPException → passes through status_code and detail
  code: "HTTP_ERROR"
- handle_generic_exception(request, exc) -> JSONResponse
  Catches all other Exception → returns 500
  detail: "An unexpected error occurred"
  code: "INTERNAL_ERROR"
  Logs the real exception message and traceback internally at ERROR level
- register_exception_handlers(app: FastAPI) -> None
  Registers all three handlers on the given app instance.
  Called from main.py at startup.
- All handlers return the APIError shape from src/models/base.py
- Never include raw exception messages in 500 responses

### src/models/base.py
Shared Pydantic v2 models used across all layers in every project.
 
Models:
 
  APIError(BaseModel):
    detail      : str   — human-readable error message
    code        : str   — machine-readable code e.g. "VALIDATION_ERROR"
    status_code : int   — HTTP status code
 
  HealthResponse(BaseModel):
    status  : str   — "ok" or "degraded"
    version : str   — app version string
    env     : str   — environment name e.g. "development"
 
### src/api/v1/deps.py
Shared FastAPI injectable dependencies used by all route handlers
across all projects.
 
Dependencies:
 
  get_trace_id(x_trace_id: str = Header(default=None)) -> str
    Returns the X-Trace-Id request header value if provided.
    Generates a fresh UUID4 string if the header is absent.
    Inject via: trace_id: str = Depends(get_trace_id)
 
  Note: get_settings() is NOT defined here — it is project-specific
  and lives in src/core/config.py which is generated per-project.
 
### src/api/v1/health.py
Standard health check endpoints — identical in every FastAPI project.
 
Endpoints:
 
  GET /v1/health
    Returns 200 HealthResponse with status "ok"
    Liveness check — is the process running?
    No external dependency checks.
 
  GET /v1/ready
    Returns 200 HealthResponse with status "ok"
    Readiness check — is the app ready to serve traffic?
    For v1: same as /health. External checks added per-project as needed.
 
  Both endpoints inject version and env from app state set at startup.
  Do not import Settings directly — receive version and env via
  app.state set in main.py.
 
## Files to generate
src/core/logging.py
src/core/errors.py
src/models/base.py
src/api/v1/deps.py
src/api/v1/health.py
 
## Behaviour
- configure_logging() is idempotent — safe to call multiple times
- All exception handlers log internally before responding to client
- get_trace_id always returns a non-empty string — never None
- health endpoints never fail — they have no external dependencies
- No project-specific imports anywhere in these files
- No openai, langchain, or langgraph imports anywhere in these files

## Acceptance criteria
- GET /v1/health returns 200 with { status: "ok", version, env }
- GET /v1/ready returns 200 with { status: "ok", version, env }
- POST to non-existent route returns 404 with APIError shape
- Invalid JSON body returns 422 with APIError shape
- Unhandled exception returns 500 with APIError — no raw traceback
- get_trace_id returns a valid UUID4 when no X-Trace-Id header sent
- get_trace_id returns the header value when X-Trace-Id is present
- Every log line produced by configure_logging is valid JSON
- No openai_api_key or any secret value ever appears in log output
- None of the generated files import from openai, langchain, langgraph