import sys
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", "vendor", ".venv", "venv",
    "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
    ".tox", ".mypy_cache", ".pytest_cache", "coverage", ".coverage",
}

PRIORITY_FILES = [
    "README.md",
    "readme.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "Dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    ".env.example",
    "main.py",
    "app.py",
    "index.ts",
    "index.js",
    "manage.py",
    "server.py",
    "Makefile",
]

SECURITY_GLOBS = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
]

CODE_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rb",
    ".rs", ".php", ".cs", ".cpp", ".c", ".h", ".swift", ".kt",
    ".vue", ".svelte",
}

MAX_CONTEXT_CHARS = 50_000
MAX_FILE_CHARS = 10_000
MAX_CODE_SAMPLES = 10


def collect_context(repo_path: Path) -> dict:
    """Collect repository context within a character budget.

    Returns:
        dict with "tree" (str) and "files" (dict of relative path -> content)
    """
    tree = build_tree(repo_path, max_depth=3)
    files = {}
    remaining = MAX_CONTEXT_CHARS - len(tree)

    def _add_file(rel_path: str, filepath: Path) -> None:
        """Read a file and add it to the collection if it fits the budget."""
        nonlocal remaining
        if rel_path in files:
            return
        content = _read_file(filepath)
        if content and len(content) <= remaining:
            files[rel_path] = content
            remaining -= len(content)

    # 1. Priority files
    for filename in PRIORITY_FILES:
        filepath = repo_path / filename
        if filepath.is_file():
            _add_file(filename, filepath)

    # 2. Security-relevant files
    for pattern in SECURITY_GLOBS:
        for filepath in repo_path.glob(pattern):
            _add_file(str(filepath.relative_to(repo_path)), filepath)

    # 3. Code samples (smaller files first, root files prioritized)
    code_files = []
    for filepath in repo_path.rglob("*"):
        if not filepath.is_file() or filepath.suffix not in CODE_EXTENSIONS:
            continue
        rel = filepath.relative_to(repo_path)
        if str(rel) in files:
            continue
        if any(part in IGNORE_DIRS or part.endswith(".egg-info") for part in rel.parts):
            continue
        code_files.append((rel, filepath.stat().st_size))

    code_files.sort(key=lambda x: (len(x[0].parts), x[1]))

    for rel, _ in code_files[:MAX_CODE_SAMPLES]:
        _add_file(str(rel), repo_path / rel)

    return {"tree": tree, "files": files}


def build_tree(repo_path: Path, max_depth: int = 3) -> str:
    """Build a text representation of the directory tree."""
    lines = []
    _walk_tree(repo_path, lines, max_depth, depth=0)
    return "\n".join(lines)


def _walk_tree(current: Path, lines: list, max_depth: int, depth: int):
    if depth >= max_depth:
        return

    try:
        entries = sorted(current.iterdir(), key=lambda e: (e.is_file(), e.name))
    except PermissionError:
        return

    for entry in entries:
        if entry.name in IGNORE_DIRS or entry.name.endswith(".egg-info"):
            continue

        indent = "  " * depth
        if entry.is_dir():
            lines.append(f"{indent}{entry.name}/")
            _walk_tree(entry, lines, max_depth, depth + 1)
        else:
            lines.append(f"{indent}{entry.name}")


def _read_file(filepath: Path) -> str:
    """Read a file safely, truncating if too large. Returns empty string on error."""
    try:
        text = filepath.read_text(encoding="utf-8", errors="replace")
        if len(text) > MAX_FILE_CHARS:
            return text[:MAX_FILE_CHARS] + f"\n\n... (truncated, {len(text)} total chars)"
        return text
    except (OSError, UnicodeDecodeError) as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return ""
