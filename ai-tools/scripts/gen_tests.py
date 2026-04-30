"""
gen_tests.py — generate tests from skills.md + spec.
Stages output in .generated/<feature>_tests/ — never touches tests/ directly.
Usage: python ai-tools/scripts/gen_tests.py --spec ai-tools/specs/spec_<name>.md
"""
import re
import argparse
from pathlib import Path
from glob import glob
from datetime import datetime
from openai import OpenAI
 
AI_TOOLS     = Path(__file__).parent.parent
REPO_ROOT    = AI_TOOLS.parent
SKILLS       = (AI_TOOLS / "skills.md").read_text()
TEMPLATE     = (AI_TOOLS / "prompts/generate_tests.md").read_text()
STAGING_ROOT = REPO_ROOT / ".generated"
 
client = OpenAI()
 
def parse_context_from_spec(spec_text: str) -> list[str]:
    match = re.search(r"##\s+Context files\s*\n(.*?)(?=\n##|\Z)", spec_text, re.DOTALL)
    if not match:
        return []
    return [l.strip() for l in match.group(1).splitlines() if l.strip() and not l.strip().startswith("#")]
 
def resolve_paths(patterns: list[str]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for pat in patterns:
        for m in sorted(glob(pat, recursive=True) or [pat]):
            p = Path(m)
            if p.is_file() and p not in seen:
                seen.add(p); result.append(p)
    return result
 
def build_context_block(paths: list[Path]) -> str:
    if not paths:
        return "None provided."
    return "\n\n".join(f"# --- FILE: {p} ---\n{p.read_text().strip()}" for p in paths)
 
def build_prompt(task: str, spec: str, context_block: str) -> str:
    return (
        TEMPLATE
        .replace("{{ skills_md }}", SKILLS)
        .replace("{{ spec }}",      spec)
        .replace("{{ task }}",      task)
        .replace("{{ context }}",   context_block)
    )
 
def generate(spec_path: str, task: str) -> None:
    spec_text     = Path(spec_path).read_text()
    context_paths = resolve_paths(parse_context_from_spec(spec_text))
    context_block = build_context_block(context_paths)
 
    spec_name = Path(spec_path).stem.replace("spec_", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging   = STAGING_ROOT / f"{spec_name}_tests" / timestamp
    staging.mkdir(parents=True, exist_ok=True)
 
    prompt = build_prompt(task, spec_text, context_block)
    print(f"  → prompt size: {len(prompt):,} chars")
 
    resp = client.chat.completions.create(
        model="gpt-4o", temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
 
    raw    = resp.choices[0].message.content
    blocks = re.split(r"#\s*===\s*FILE:\s*(.+?)\s*===", raw)
    pairs  = list(zip(blocks[1::2], blocks[2::2]))
    written: list[Path] = []
    for rel, code in pairs:
        dest = staging / rel.strip()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(code.strip() + "\n")
        print(f"  staged  → {dest}")
        written.append(Path(rel.strip()))
 
    lines = ["# Generated manifest", f"spec: {spec_path}",
             f"generated: {datetime.now().isoformat()}", "status: pending", "", "## Files"] + [str(f) for f in written]
    (staging / "manifest.md").write_text("\n".join(lines) + "\n")
    print(f"\n  ✓ review, then: python ai-tools/scripts/promote.py --staging {staging}")
    
 
if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--spec", required=True)
    p.add_argument("--task", default="Generate tests for every acceptance criterion in <Spec>.")
    args = p.parse_args()
    generate(args.spec, args.task)