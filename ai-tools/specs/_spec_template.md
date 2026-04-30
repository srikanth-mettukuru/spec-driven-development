# Spec: <feature name>
 
## Meta
- Feature   : <short name>
- Endpoint  : <METHOD> /v1/<path>
- Author    : <name>
- Status    : draft | ready for codegen | done

## Context files
# Paths relative to repo root. Loaded automatically by gen_code.py.
# Add files the LLM must read before generating.
src/core/config.py
src/core/logging.py
src/models/base.py
src/api/v1/deps.py
 
## Summary
<2-3 sentences describing what this feature does>
 
## Request
Method  : <GET|POST|PUT|DELETE>
Path    : /v1/<path>
Headers : Content-Type: application/json
 
Body (JSON):
  field_name : type — description (required/optional, constraints)
 
## Response
Success (<status_code>):
  <response shape>
 
Errors:
  422 — <validation failure condition>
  503 — <service unavailable condition>
 
Error body shape:
  { "detail": "<message>", "code": "<error_code>", "status_code": <int> }
 
## Behaviour
- <rule 1 — retry / logging / streaming / degradation etc>
- <rule 2>

## Files to generate
src/api/v1/<feature>.py
src/services/<feature>_service.py
src/models/<feature>.py
 
## Acceptance criteria
- <condition> → <expected result>
- <condition> → <expected result>