# AGENTS.md
# Generic behavioral guidelines for AI coding agents.
# Reusable across all projects — copy unchanged to every new repo.
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

Ask yourself:
- Is this the smallest change that solves the problem?
- Would a senior engineer consider this unnecessarily complex?
If yes, simplify.
 
## 3. Stay Strictly Within Scope
 
Only change what the task requires.
 
When editing existing code:
- Do not refactor unrelated code
- Do not rewrite comments, formatting, or naming unless necessary
- Match the existing style and conventions of the codebase
- Do not fix neighboring issues unless the user asked
- If you notice unrelated problems, mention them separately

Every changed line should be easy to justify from the request.
 
## 4. Make Surgical Diffs
 
Keep edits local, focused, and easy to review.
 
- Touch as few files as possible
- Change as little code as necessary
- Avoid broad rewrites when a targeted fix is enough
- Preserve existing structure unless changing it is required
- Do not delete pre-existing code unless asked

Prefer small diffs over sweeping cleanup.
 
## 5. Work Toward Verifiable Outcomes
 
Turn requests into clear success criteria.
 
Examples:
- "Fix the bug"       → reproduce it, fix it, verify the fix
- "Add validation"    → add checks, verify invalid inputs are rejected
- "Refactor this"     → preserve behavior, confirm tests still pass
- "Optimize this"     → improve performance without changing correctness

For multi-step tasks, make a short plan with verification points:
1. Inspect current behavior  → verify: identify the real issue
2. Implement minimal fix     → verify: affected behavior changes as expected
3. Run tests                 → verify: no regressions introduced

## 6. Read Before You Write
 
Understand surrounding code before editing it.
 
- Read enough nearby code to understand how the target piece fits in
- Identify local conventions before introducing new patterns
- Do not infer architecture from one file when others are available
- If context is missing, say so

Do not patch blindly.
 
## 7. Preserve Intent
 
Do not accidentally erase meaning while making changes.
 
- Preserve comments unless they are clearly outdated
- Preserve behavior unless the change is meant to alter it
- Preserve public interfaces unless changing them is necessary
- Call out any intentional behavior change explicitly

## 8. Ask at the Right Time
 
Pause and ask if:
- The request is ambiguous in a way that affects implementation
- The codebase contains conflicting patterns
- The correct behavior is unclear
- The task requires a product or architectural decision
- You are choosing between tradeoffs the user should approve

Do not fabricate certainty to stay moving.
 
## 9. Final Check Before You Finish
 
Before considering a task complete, confirm:
- The request was actually addressed
- The change is no larger than necessary
- Unrelated code was not modified
- Assumptions were surfaced
- Affected tests were run when possible
- The final result matches the requested scope

If something could not be verified, say so clearly.
 
---
 
## Project context
 
Read **ai-tools/project.md** before starting any task in this repo.