# project.md
# Project-specific context for interactive coding agents.
# Read by: Claude Code, GitHub Copilot, Cursor, Windsurf, Amp, Gemini CLI
# Loaded via pointer in AGENTS.md / CLAUDE.md at session start.
# NOT injected into code generation prompts — see ai-tools/skills.md for that.
 
---
 
## What this project is
 
A simple Agentic AI API built with FastAPI.
Exposes REST endpoints that internally route requests through a
LangGraph agent which uses an LLM (OpenAI) for reasoning.
LangChain handles prompt templating, memory, and tool wiring.
The API is stateless externally — agent state is managed internally
per request via LangGraph's in-memory state machine.
 
---
 
## Stack
 
| Layer        | Technology                          |
|--------------|-------------------------------------|
| Language     | Python 3.11+                        |
| API          | FastAPI + Pydantic v2               |
| Agent        | LangGraph (state machine)           |
| Chains       | LangChain (prompts, memory, tools)  |
| LLM          | OpenAI (gpt-4o default)             |
| Config       | pydantic-settings + .env            |
| Testing      | pytest + pytest-asyncio             |
| Linting      | ruff                                |
| Type check   | mypy                                |


---
 
## Commands
 
```
# Setup
pip install -e ".[dev]"
cp .env.example .env          # then fill in OPENAI_API_KEY
 
# Run
uvicorn src.main:app --reload
 
# Test
pytest
pytest --cov=src --cov-report=term-missing
 
# Lint / format / typecheck
ruff check src tests
ruff format src tests
mypy src
```
 
---
 
## Folder ownership — know this before touching anything
 
```
src/api/v1/         FastAPI routes ONLY — no business logic here
src/agents/         LangGraph graph, nodes, and MCP tool definitions
src/services/       LLM calls, retry logic, streaming, logging
src/models/         Shared Pydantic models (request/response/error shapes)
src/core/           Config (pydantic-settings), logging, error handlers
src/main.py         FastAPI app entry point — router registration only
 
tests/unit/         Service and model tests — LLM always mocked
tests/integration/  Endpoint tests via FastAPI TestClient — LLM mocked
tests/e2e/          Full stack tests — gated to staging, not every PR
 
ai-tools/           Dev-time AI tooling — NEVER imported by src/
ai-tools/project.md This file — project context for interactive agents
ai-tools/skills.md  Coding conventions — injected into gen prompts only
ai-tools/specs/     One spec per feature — drives code + test generation
ai-tools/scripts/   gen_code.py, gen_tests.py, promote.py
 
docs/               Human-readable architecture docs
.generated/         Staging area for generated code — GITIGNORED
```
 
**Hard rules:**
- `src/` is never touched during a code generation run — use the scripts
- `ai-tools/` is never imported by `src/` — it never ships to production
- `.generated/` is never committed — it is gitignored for a reason
---
 
## Spec-driven development workflow
 
This project uses spec-driven code generation. Follow this — do not bypass it.
 
```bash
# Step 1 — generate code (stages in .generated/, never touches src/)
python ai-tools/scripts/gen_code.py \
  --spec ai-tools/specs/spec_<feature>.md
 
# Step 2 — review staged files in .generated/<feature>/<timestamp>/
 
# Step 3 — dry run to see what will be written
python ai-tools/scripts/promote.py \
  --staging .generated/<feature>/<timestamp>/ \
  --dry-run
 
# Step 4 — promote reviewed files to src/
python ai-tools/scripts/promote.py \
  --staging .generated/<feature>/<timestamp>/
 
# Step 5 — generate tests from the same spec
python ai-tools/scripts/gen_tests.py \
  --spec ai-tools/specs/spec_<feature>.md
 
# Step 6 — promote tests, run pytest, commit
pytest tests/
git add -p
git commit -m "feat: <feature> (from spec_<feature>.md)"
```
 
---
 
## Architecture — how a request flows
 
```
Client
  └─► POST /v1/agent/run
        └─► src/api/v1/agent.py        (route — thin, validates input)
              └─► src/services/agent_service.py   (orchestration)
                    └─► src/agents/graph.py        (LangGraph state machine)
                          ├─► src/agents/nodes.py  (planner, executor, responder)
                          └─► src/agents/tools.py  (tool definitions)
                                └─► OpenAI via src/services/llm_service.py
```
 
---
 
## Security — non-negotiable
 
- Never hardcode secrets — always use `src/core/config.py` + environment variables
- `OPENAI_API_KEY` lives in `.env` only — never in code or logs
- Never log raw LLM output or raw user messages — log summaries only
- Never expose raw upstream error messages to API clients
- `.env` is gitignored — use `.env.example` as the committed template
- Never commit anything from `.generated/`
---
 
## Environment variables (see .env.example)
 
```
OPENAI_API_KEY=        # required
OPENAI_MODEL=gpt-4o    # optional, default gpt-4o
MAX_TOKENS=1000         # optional, default 1000
LOG_LEVEL=INFO          # optional, default INFO
APP_ENV=development     # development | staging | production
```