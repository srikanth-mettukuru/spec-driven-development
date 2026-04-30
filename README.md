# spec-driven-development
 
A lean, production-ready scaffold for building **Agentic AI APIs** using spec-driven development.
 
The idea: write a spec for each feature, run a script, review the generated code in a staging area, then promote it into the repo. No code is written by hand during a generation run.
 
---
 
## What this project is
 
A **FastAPI + LangGraph** backend that exposes REST endpoints backed by a stateful LangGraph agent. The agent uses OpenAI for reasoning and LangChain for prompt templating. All application code is generated from feature specs — not written manually.
 
---
 
## Stack
 
| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| API | FastAPI + Pydantic v2 |
| Agent | LangGraph |
| Chains / Prompts | LangChain |
| LLM | OpenAI (gpt-4o) |
| Config | pydantic-settings + `.env` |
| Testing | pytest + pytest-asyncio |
| Linting | ruff |
| Type checking | mypy |
| Package manager | uv |
 
---
 
## Repository structure
 
```
spec-driven-development/
│
├── AGENTS.md              ← generic agent behavior rules (reusable across projects)
├── CLAUDE.md              ← same rules + Claude Code specific additions
├── README.md              ← this file
│
├── src/                   ← application code (generated from specs, not hand-written)
│   ├── main.py
│   ├── api/v1/            ← FastAPI routes (thin layer only)
│   ├── agents/            ← LangGraph graph, nodes, tools
│   ├── services/          ← LLM calls, retry, logging
│   ├── models/            ← shared Pydantic models
│   └── core/              ← config, logging, error handlers
│
├── tests/                 ← generated from same spec as code
│   ├── conftest.py
│   ├── unit/
│   └── integration/
│
├── ai-tools/              ← dev-time AI tooling (never imported by src/, never deployed)
│   ├── project.md         ← project context for interactive coding agents
│   ├── skills.md          ← coding conventions injected into gen prompts
│   ├── prompts/           ← generate_code.md and generate_tests.md templates
│   ├── specs/             ← one spec per feature
│   │   ├── _spec_template.md
│   │   └── spec_agent_run.md
│   └── scripts/
│       ├── gen_code.py    ← generates code → stages in .generated/
│       ├── gen_tests.py   ← generates tests → stages in .generated/
│       └── promote.py     ← promotes staged files → src/ or tests/
│
├── .generated/            ← gitignored staging area (never commit this)
├── docs/
│   └── architecture.md
├── pyproject.toml
├── Dockerfile
├── .env.example
└── .gitignore
```
 
---
 
## How the AI tooling layer works
 
Three files, three distinct purposes, three different consumers:
 
| File | Read by | Purpose |
|------|---------|---------|
| `AGENTS.md` / `CLAUDE.md` | Interactive coding agents (Copilot, Claude Code, Cursor…) | Generic behavioral rules — how to work in any project |
| `ai-tools/project.md` | Interactive coding agents (via pointer in AGENTS.md) | Project-specific context — commands, folders, security rules |
| `ai-tools/skills.md` | `gen_code.py` / `gen_tests.py` scripts | Coding conventions injected into every LLM generation prompt |
 
---
 
## Getting started
 
### 1. Clone and set up
 
```bash
git clone https://github.com/srikanth-mettukuru/spec-driven-development.git
cd spec-driven-development
 
uv pip install -e ".[dev]"
 
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```
 
### 2. Write a spec
 
Copy the blank template and fill it in:
 
```bash
cp ai-tools/specs/_spec_template.md ai-tools/specs/spec_<feature>.md
```
 
Each spec declares:
- What the feature does (summary, request/response shapes)
- Which existing files the LLM should read first (context files)
- Which files to generate
- Acceptance criteria (each one becomes a test case)
### 3. Generate code
 
```bash
python ai-tools/scripts/gen_code.py \
  --spec ai-tools/specs/spec_<feature>.md
```
 
Output is staged in `.generated/<feature>/<timestamp>/` — `src/` is never touched.
 
### 4. Review
 
Open the staged folder in your editor. Edit if needed. Then dry-run to see what will be written:
 
```bash
python ai-tools/scripts/promote.py \
  --staging .generated/<feature>/<timestamp>/ \
  --dry-run
```
 
### 5. Promote
 
```bash
python ai-tools/scripts/promote.py \
  --staging .generated/<feature>/<timestamp>/
```
 
### 6. Generate tests from the same spec
 
```bash
python ai-tools/scripts/gen_tests.py \
  --spec ai-tools/specs/spec_<feature>.md
```
 
Review, promote, then run:
 
```bash
pytest tests/
git add -p
git commit -m "feat: <feature> (from spec_<feature>.md)"
```
 
---
 
## Development commands
 
```bash
# Install all dependencies
uv pip install -e ".[dev]"
 
# Run the app
uvicorn src.main:app --reload
 
# Run tests
pytest
 
# Run tests with coverage
pytest --cov=src --cov-report=term-missing
 
# Lint
ruff check src tests
 
# Format
ruff format src tests
 
# Type check
mypy src
```
 
---
 
## Key rules
 
- **Never manually edit `src/` during a generation run** — always use the scripts
- **Never commit `.generated/`** — it is gitignored for a reason
- **Never commit `.env`** — use `.env.example` as the template
- **`ai-tools/` is never imported by `src/`** — it never ships to production
- **Mock all LLM calls in tests** — never hit live APIs in CI
---
 
## How a request flows
 
```
Client
  └─► POST /v1/agent/run
        └─► src/api/v1/agent.py        (route — validates input only)
              └─► src/services/agent_service.py   (orchestration)
                    └─► src/agents/graph.py        (LangGraph state machine)
                          ├─► src/agents/nodes.py  (planner, executor, responder)
                          └─► src/services/llm_service.py  (OpenAI wrapper)
```
 
---
 
## Environment variables
 
See `.env.example` for the full list. Required:
 
```
OPENAI_API_KEY=your-key-here
```
 
Optional (with defaults):
 
```
OPENAI_MODEL=gpt-4o
MAX_TOKENS=1000
LOG_LEVEL=INFO
APP_ENV=development
```
 
---
 
## Related reading
 
- `ai-tools/project.md` — full project context for interactive coding agents
- `ai-tools/skills.md` — coding conventions used during code generation
- `docs/architecture.md` — system design and design decisions