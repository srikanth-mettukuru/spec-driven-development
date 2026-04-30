# CLAUDE.md
# Behavioral guidelines for Claude Code specifically.
# Generic rules are identical to AGENTS.md.
# For project-specific context, read ai-tools/project.md first.
 
---
 
## 1. Think Before You Code
 
Do not silently guess.
 
Before making changes:
- State your assumptions clearly
- If anything is ambiguous, ask instead of choosing silently
- If multiple valid approaches exist, briefly present the tradeoff
- If the request seems mistaken or overcomplicated, say so
- If a simpler solution exists, recommend it before implementing
- If you are confused, stop and explain what is unclear
Do not act certain when you are uncertain.
 
## 2. Keep the Solution Simple
 
Solve the requested problem with the minimum necessary code.
 
- Do not add features that were not asked for
- Do not introduce abstractions for one-time use
- Do not add configurability or generalization unless requested
- Prefer simple, readable code over clever code
- If the solution feels too large, step back and simplify it

## 3. Stay Strictly Within Scope
 
Only change what the task requires.
 
- Do not refactor unrelated code
- Match the existing style and conventions of the codebase
- Do not fix neighboring issues unless the user asked
- Mention unrelated problems separately instead of changing them

## 4. Make Surgical Diffs
 
- Touch as few files as possible
- Change as little code as necessary
- Avoid broad rewrites when a targeted fix is enough
- Do not delete pre-existing code unless asked

## 5. Work Toward Verifiable Outcomes
 
Turn requests into clear success criteria. For multi-step tasks,
make a short plan with verification points before starting.
 
## 6. Read Before You Write
 
- Read enough nearby code to understand how the target fits in
- Identify local conventions before introducing new patterns
- Use the Read tool before Edit — always understand before changing

## 7. Preserve Intent
 
- Preserve comments unless clearly outdated
- Preserve behavior unless the change is meant to alter it
- Call out any intentional behavior change explicitly

## 8. Ask at the Right Time
 
Pause and ask if the request is ambiguous, the codebase has
conflicting patterns, or the task requires an architectural decision.
 
## 9. Final Check Before You Finish
 
Confirm: request addressed · change minimal · unrelated code untouched
· assumptions surfaced · tests run · scope matched.
 
---
 
## Claude Code specific
 
- Always use the Read tool to inspect a file before editing it
- Run `pytest` after every code change — report failures before proceeding
- When generating code via spec, use the scripts in ai-tools/scripts/
  Do NOT directly edit src/ during a generation run
- Prefer `uv` over `pip` for package management in this project
- If unsure about scope, ask rather than guess
---
 
## Project context
 
Read **ai-tools/project.md** before starting any task in this repo.