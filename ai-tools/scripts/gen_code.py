"""
gen_code.py — generate code from skills.md + spec.
Stages output in .generated/ — never touches src/ directly.
Usage: python ai-tools/scripts/gen_code.py --spec ai-tools/specs/spec_<name>.md
"""
import re
import argparse
from pathlib import Path
from glob import glob
from datetime import datetime
from openai import OpenAI
 
AI_TOOLS    = Path(__file__).parent.parent
REPO_ROOT   = AI_TOOLS.parent
SKILLS      = (AI_TOOLS / "skills.md").read_text()
TEMPLATE    = (AI_TOOLS / "prompts/generate_code.md").read_text()
STAGING_ROOT = REPO_ROOT / ".generated"
 
client = OpenAI()
 
# ── context helpers ────────────────────────────────────────────────────
 
def parse_context_from_spec(spec_text: str) -> list[str]:
    """Extract file paths from '## Context files' section in the spec."""
    match = re.search(r"##\s+Context files\s*\n(.*?)(?=\n##|\Z)", spec_text, re.DOTALL)
    if not match:
        return []
    return [
        line.strip()
        for line in match.group(1).splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
 
def resolve_paths(patterns: list[str]) -> list[Path]:
    """Expand globs, deduplicate, return Paths that exist."""
    seen: set[Path] = set()
    result: list[Path] = []
    for pat in patterns:
        for m in sorted(glob(pat, recursive=True) or [pat]):
            p = Path(m)
            if p.is_file() and p not in seen:
                seen.add(p)
                result.append(p)
    return result
 
def build_context_block(paths: list[Path]) -> str:
    """Wrap each file in a labelled header so the LLM knows the source."""
    if not paths:
        return "None provided."
    return "\n\n".join(f"# --- FILE: {p} ---\n{p.read_text().strip()}" for p in paths)
 
# ── prompt ─────────────────────────────────────────────────────────────
 
def build_prompt(task: str, spec: str, context_block: str) -> str:
    return (
        TEMPLATE
        .replace("{{ skills_md }}", SKILLS)
        .replace("{{ spec }}",      spec)
        .replace("{{ task }}",      task)
        .replace("{{ context }}",   context_block)
    )
 
# ── staging ────────────────────────────────────────────────────────────
 
def make_staging_dir(spec_path: str) -> Path:
    """Create .generated/<feature>/<timestamp>/"""
    spec_name = Path(spec_path).stem.replace("spec_", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging   = STAGING_ROOT / spec_name / timestamp
    staging.mkdir(parents=True, exist_ok=True)
    return staging
 
def write_files(raw: str, staging_dir: Path) -> list[Path]:
    """Parse FILE markers and write to staging."""
    blocks = re.split(r"#\s*===\s*FILE:\s*(.+?)\s*===", raw)
    pairs  = list(zip(blocks[1::2], blocks[2::2]))
    if not pairs:
        print("  ⚠ no FILE markers — writing raw.txt to staging")
        (staging_dir / "raw.txt").write_text(raw)
        return []
    written = []
    for rel, code in pairs:
        dest = staging_dir / rel.strip()
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(code.strip() + "\n")
        print(f"  staged  → {dest}")
        written.append(Path(rel.strip()))
    return written
 
def write_manifest(staging_dir: Path, spec_path: str, files: list[Path]) -> None:
    """Write manifest.md — promote.py reads this."""
    lines = [
        "# Generated manifest",
        f"spec: {spec_path}",
        f"generated: {datetime.now().isoformat()}",
        "status: pending",
        "",
        "## Files",
    ] + [str(f) for f in files]
    (staging_dir / "manifest.md").write_text("\n".join(lines) + "\n")
    print(f"  manifest → {staging_dir}/manifest.md")
 
# ── main ───────────────────────────────────────────────────────────────
 
def generate(spec_path: str, task: str) -> None:
    spec_text     = Path(spec_path).read_text()
    context_paths = resolve_paths(parse_context_from_spec(spec_text))
    context_block = build_context_block(context_paths)
 
    if context_paths:
        print(f"  → context: {len(context_paths)} file(s) from spec")
        for p in context_paths:
            print(f"      {p}")
    else:
        print("  → context: none declared in spec")
 
    prompt = build_prompt(task, spec_text, context_block)
    print(f"  → prompt size: {len(prompt):,} chars")
 
    resp = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}],
    )
 
    staging_dir = make_staging_dir(spec_path)
    print(f"\n  → staging: {staging_dir}")
    written = write_files(resp.choices[0].message.content, staging_dir)
    write_manifest(staging_dir, spec_path, written)
    print(f"\n  ✓ review output, then run:")
    print(f"    python ai-tools/scripts/promote.py --staging {staging_dir}")
 
 
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Generate code from skills.md + spec")
    p.add_argument("--spec", required=True, help="Path to spec file")
    p.add_argument("--task", default="Implement the feature described in <Spec>.")
    args = p.parse_args()
    generate(args.spec, args.task)