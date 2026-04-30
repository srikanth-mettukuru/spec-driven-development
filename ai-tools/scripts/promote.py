"""
promote.py — promote staged generated files into the repo.
Usage: python ai-tools/scripts/promote.py --staging .generated/<f>/<ts>/
       python ai-tools/scripts/promote.py --staging .generated/<f>/<ts>/ --dry-run
       python ai-tools/scripts/promote.py --staging .generated/<f>/<ts>/ --force
"""
import re
import argparse
import shutil
from pathlib import Path
from datetime import datetime
 
REPO_ROOT = Path(__file__).parent.parent.parent
 
def read_manifest(staging_dir: Path) -> tuple[str, list[Path]]:
    manifest = (staging_dir / "manifest.md").read_text()
    spec     = re.search(r"^spec:\s*(.+)$", manifest, re.M).group(1).strip()  # type: ignore[union-attr]
    section  = re.search(r"## Files\n(.*)", manifest, re.DOTALL)
    files    = [
        Path(line.strip())
        for line in section.group(1).splitlines()  # type: ignore[union-attr]
        if line.strip() and not line.strip().startswith("#")
    ]
    return spec, files
 
def promote(staging_dir: Path, force: bool, dry_run: bool) -> None:
    spec_path, files = read_manifest(staging_dir)
    print(f"  spec    : {spec_path}")
    print(f"  staging : {staging_dir}")
    print(f"  files   : {len(files)}")
    if dry_run:
        print("  mode    : dry-run (nothing will be written)\n")
 
    conflicts = [f for f in files if (REPO_ROOT / f).exists()]
 
    if conflicts and not force:
        print("\n  ⚠ the following files already exist in the repo:")
        for c in conflicts:
            print(f"      {c}")
        print("\n  run with --force to overwrite, or resolve manually.")
        return
 
    for rel in files:
        src  = staging_dir / rel
        dest = REPO_ROOT / rel
        if dry_run:
            action = "overwrite" if dest.exists() else "create"
            print(f"  [{action}] {dest}")
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        print(f"  promoted → {dest}")
 
    if not dry_run:
        m = (staging_dir / "manifest.md").read_text()
        (staging_dir / "manifest.md").write_text(
            m.replace("status: pending", f"status: promoted {datetime.now().isoformat()}")
        )
        print(f"\n  ✓ promoted {len(files)} file(s) to repo")
        print(f"  next: pytest tests/ && git add -p")
 
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Promote staged files into the repo")
    p.add_argument("--staging", required=True, help="Path to .generated/<f>/<ts>/ folder")
    p.add_argument("--force",   action="store_true", help="Overwrite existing files")
    p.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = p.parse_args()
    promote(Path(args.staging), args.force, args.dry_run)