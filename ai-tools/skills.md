# skills.md
# Coding conventions for LLM code generation.
# Injected into prompts by gen_code.py and gen_tests.py via {{ skills_md }}.
# Written for: a batch LLM generating Python files from scratch.
# NOT for interactive agents — see ai-tools/project.md for that.
 
---
 
## Programming
 
- Primary language: Python 3.11+
- Type hints on ALL functions and class attributes — no untyped code
- Use `async`/`await` for all I/O-bound operations
- Use modular layered architecture: routes → services → agents → models
- Follow clean code and SOLID principles
- Write docstrings on all public functions, classes, and modules
- Use meaningful variable names — no single-letter names outside loops
- Prefer explicit over implicit — never rely on side effects
---
 
## API development
 
- Use FastAPI for all REST and async APIs
- Validate ALL request and response shapes with Pydantic v2 models
- Use FastAPI dependency injection for shared resources (config, trace_id, auth)
- Version all routes — prefix with `/v1/`
- Return consistent error shapes across all endpoints:
  `{ "detail": "<message>", "code": "<error_code>", "status_code": <int> }`
- Use FastAPI background tasks for non-blocking side effects
- Add OpenAPI `summary`, `description`, and `response_model` to every endpoint
- Routes must be thin — no business logic in route handlers
---
 
## Agent and LangGraph design
 
- Use LangGraph for all stateful multi-step agent workflows
- Define graph in `src/agents/graph.py` — nodes in `src/agents/nodes.py`
- One concern per node — never mix responsibilities in a single node
- Use `TypedDict` for ALL state schemas — no untyped or dict state
- Entry point must be declared explicitly — never rely on implicit first node
- Handle tool call failures inside the node — return error state, do not raise
- Nodes must be `async` functions: `async def node_name(state: AgentState) -> AgentState`
- Nodes must be idempotent where possible — safe to retry on failure
---
 
## LangChain usage
 
- Use LangChain for prompt templates, output parsers, and memory
- Use `ChatPromptTemplate` for all LLM prompt construction
- Use `StrOutputParser` or a typed `PydanticOutputParser` — never parse raw strings
- Keep prompt templates in dedicated variables — never inline in logic code
- Memory is per-request only — no cross-request shared memory in this project
---
 
## LLM integration
 
- Use OpenAI SDK via LangChain's `ChatOpenAI` wrapper
- Abstract the LLM client behind a service — never instantiate directly in routes or nodes
- Always stream responses for user-facing latency-sensitive paths
- Implement retry logic with exponential backoff on rate limit errors (429)
- Log per LLM call: `trace_id`, `model`, `input_tokens`, `output_tokens`, `latency_ms`
- Never hardcode model names — read from `settings.openai_model`
- Graceful degradation when LLM is unavailable — return 503 with structured error
---
 
## Data models
 
- All request/response models live in `src/models/`
- Use Pydantic v2 `model_validator` and `field_validator` for complex validation
- Shared error model `APIError` must be imported from `src/models/base.py`
- Field names must match the spec exactly — no renaming
- Use `model_config = ConfigDict(...)` not the deprecated `class Config`
---
 
## Testing
 
- Use `pytest` for ALL unit and integration tests
- Use `pytest-asyncio` for all async test cases — annotate with `@pytest.mark.asyncio`
- Mock ALL LLM and OpenAI calls in tests — never hit live APIs in CI
- Use `unittest.mock.AsyncMock` for async service mocks
- Use FastAPI `TestClient` for endpoint integration tests
- Follow AAA pattern strictly — Arrange, Act, Assert — one blank line between each
- Test both valid and invalid inputs for every Pydantic model
- Target 80%+ coverage on all core business logic in `src/services/` and `src/agents/`
- Test file naming: `test_<module_name>.py` — mirrors the src/ structure
---
 
## Observability
 
- Use structured JSON logging — every log line must include `trace_id`
- `trace_id` is generated per request in `src/api/v1/deps.py` and propagated through all layers
- Log levels: DEBUG for trace/detail, INFO for normal operations, ERROR for failures
- Never log raw LLM output, raw user input, or API keys
- Expose `/health` (liveness) and `/ready` (readiness) endpoints in `src/api/v1/health.py`
- Implement circuit breakers on all external LLM API calls
---
 
## Configuration
 
- All config lives in `src/core/config.py` using `pydantic-settings`
- Config is loaded once at startup via a `get_settings()` dependency
- Never read `os.environ` directly — always go through `settings`
- All secrets come from environment variables — never hardcoded
---
 
## Error handling
 
- Global exception handlers live in `src/core/errors.py`
- Never expose raw upstream error messages to API clients
- All unhandled exceptions must be caught by the global handler and returned
  as a structured `APIError` response
- LLM errors must be caught in the service layer — never bubble to routes raw
---
 
## Decision making
 
- Choose the simplest tool that meets the requirement
- Prefer `async` over sync for all network or LLM-bound operations
- Avoid vendor lock-in — keep LLM provider abstracted behind a service interface
- Fail fast and loudly in development, degrade gracefully in production
- Do not use any library not listed in the project stack