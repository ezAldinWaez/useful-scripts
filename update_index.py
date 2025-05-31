"""
Walks the scripts/ directory, reads the first heading + Purpose section
from each README.md, and rewrites the repo-root README.md with a table index.
"""
from pathlib import Path
import re
import textwrap

ROOT = Path(__file__).resolve().parent
SCRIPTS_DIR = ROOT / "scripts"
README_ROOT = ROOT / "README.md"


def extract_meta(readme_path: Path):
    md = readme_path.read_text(encoding="utf-8")
    # First heading (script title)
    title = re.search(r"^#\s+(.+)", md, re.M).group(1).strip()
    # Purpose section (first paragraph under "## Purpose")
    purpose = re.search(r"##\s+Purpose\n(.+?)(?:\n##|\Z)", md, re.S)
    purpose = re.sub(r"\s+", " ", purpose.group(1).strip()) if purpose else ""
    # Language (fallback to dir name extension)
    lang = re.search(r"\*\*Language:\*\*\s*`([^`]+)`", md)
    lang = lang.group(1) if lang else readme_path.parent.glob(
        "*.*").__iter__().__next__().suffix.lstrip(".")
    return title, lang, purpose[:80] + ("…" if len(purpose) > 80 else "")


def build_table():
    rows = []
    for sub in sorted(SCRIPTS_DIR.iterdir()):
        rd = sub / "README.md"
        if rd.exists():
            title, lang, descr = extract_meta(rd)
            link = f"[{title}]({rd.relative_to(ROOT).parent})"
            rows.append(f"| {link} | {lang} | {descr} |")
    header = textwrap.dedent("""\
        # useful-scripts

        A grab-bag of bite-size utilities I’ve written for everyday tasks.  
        *Every script lives in `scripts/<name>/` and has its own README.*

        | Script | Language | Short description |
        |--------|----------|-------------------|
    """)
    README_ROOT.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")


if __name__ == "__main__":
    build_table()
    print("README.md regenerated ✔")
