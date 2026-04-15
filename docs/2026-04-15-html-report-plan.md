# HTML Report Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate a visually appealing HTML report (Gradient Dark theme) alongside the existing Markdown report, by parsing the MD sections and injecting them into a styled HTML template.

**Architecture:** New module `html_report.py` parses the 6 known Markdown sections via regex, converts each to HTML with the `markdown` library, and injects them into a template with semantic structure (header, metrics cards, section cards). A separate `style.css` file provides the Gradient Dark theme. `main.py` calls the new module after writing the MD report.

**Tech Stack:** Python `markdown` library (with `tables` extension), CSS3 (gradients, grid, flexbox)

---

## File Structure

```
src/repo_analyzer/
├── html_report.py   # NEW: parse MD sections, generate HTML from template
├── style.css        # NEW: Gradient Dark CSS theme
├── main.py          # MODIFY: add HTML generation after MD write
├── (other files unchanged)

pyproject.toml       # MODIFY: add markdown dependency
```

---

### Task 1: Add markdown dependency

**Files:**
- Modify: `repo-analyzer/pyproject.toml`

- [ ] **Step 1: Add markdown to dependencies**

In `repo-analyzer/pyproject.toml`, change the dependencies list from:

```toml
dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
]
```

to:

```toml
dependencies = [
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "markdown>=3.5",
]
```

- [ ] **Step 2: Install the new dependency**

```bash
cd /home/tfb/projects/repo-analyzer
source .venv/bin/activate
pip install -e .
```

Expected: `markdown` installs successfully.

- [ ] **Step 3: Verify import**

```bash
python -c "import markdown; print(f'markdown {markdown.__version__}')"
```

Expected: prints version like `markdown 3.7`.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml
git commit -m "feat: add markdown dependency for HTML report generation"
```

---

### Task 2: Create style.css

**Files:**
- Create: `repo-analyzer/src/repo_analyzer/style.css`

- [ ] **Step 1: Create the CSS file**

Create `repo-analyzer/src/repo_analyzer/style.css`:

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color: #e2e8f0;
  font-family: -apple-system, system-ui, 'Segoe UI', sans-serif;
  min-height: 100vh;
  padding: 40px 20px;
}

.container { max-width: 900px; margin: 0 auto; }

/* Header */
.report-header { margin-bottom: 32px; }

.report-header .repo-name {
  font-size: 32px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-header .repo-name .icon {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  flex-shrink: 0;
}

.report-header .repo-url {
  color: #94a3b8;
  font-size: 14px;
  margin-top: 4px;
  margin-left: 52px;
}

/* Metrics */
.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.metric {
  background: rgba(255,255,255,0.03);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
}

.metric .label {
  font-size: 12px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric .value {
  font-size: 28px;
  font-weight: 700;
  margin-top: 4px;
}

.metric .value.red { color: #f87171; }
.metric .value.amber { color: #fbbf24; }

/* Cards */
.card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 20px;
}

.card h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #f1f5f9;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card h2 .section-num {
  background: linear-gradient(135deg, #06b6d4, #8b5cf6);
  color: white;
  width: 28px; height: 28px;
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

.card p, .card li {
  color: #cbd5e1;
  line-height: 1.7;
  font-size: 14px;
}

.card ul { padding-left: 20px; }
.card li { margin-bottom: 4px; }

/* Tables */
table { width: 100%; border-collapse: collapse; margin-top: 12px; }

th {
  text-align: left;
  font-size: 11px;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  padding: 10px 12px;
  border-bottom: 1px solid #334155;
}

td {
  padding: 12px;
  font-size: 13px;
  color: #cbd5e1;
  border-bottom: 1px solid rgba(51,65,85,0.5);
  vertical-align: top;
}

tr:last-child td { border-bottom: none; }
td strong { color: #f1f5f9; }

/* Code blocks */
pre {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 8px;
  padding: 16px;
  overflow-x: auto;
  font-size: 13px;
  line-height: 1.5;
  color: #94a3b8;
}

code {
  background: rgba(51,65,85,0.5);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}

pre code {
  background: none;
  padding: 0;
}

/* Footer */
footer {
  text-align: center;
  color: #475569;
  font-size: 12px;
  margin-top: 40px;
  padding-bottom: 20px;
}
```

- [ ] **Step 2: Verify file is readable from Python**

```bash
cd /home/tfb/projects/repo-analyzer
source .venv/bin/activate
python -c "
from pathlib import Path
css = (Path('src/repo_analyzer/style.css')).read_text()
print(f'CSS loaded: {len(css)} chars')
"
```

Expected: prints `CSS loaded: NNNN chars`.

- [ ] **Step 3: Commit**

```bash
git add src/repo_analyzer/style.css
git commit -m "feat: add Gradient Dark CSS theme for HTML reports"
```

---

### Task 3: Create html_report.py

**Files:**
- Create: `repo-analyzer/src/repo_analyzer/html_report.py`

- [ ] **Step 1: Create html_report.py**

Create `repo-analyzer/src/repo_analyzer/html_report.py`:

```python
import re
from pathlib import Path

import markdown


SECTION_PATTERN = re.compile(r"^## \d+\.\s+", re.MULTILINE)

SECTION_IDS = ["summary", "tech-stack", "structure", "quality", "improvements", "security"]

SECTION_TITLES = [
    "Project Summary",
    "Tech Stack",
    "Structure & Architecture",
    "Code Quality",
    "Suggested Improvements",
    "Security Issues",
]


def generate_html(markdown_content: str, repo_name: str) -> str:
    """Parse a Markdown report and generate a styled HTML page.

    Args:
        markdown_content: The full Markdown report with 6 sections.
        repo_name: Repository name for the page header.

    Returns:
        Complete HTML document as a string.
    """
    sections = _parse_sections(markdown_content)
    return _build_html(repo_name, sections)


def get_stylesheet() -> str:
    """Return the content of the CSS stylesheet."""
    css_path = Path(__file__).parent / "style.css"
    return css_path.read_text(encoding="utf-8")


def _parse_sections(markdown_content: str) -> list[str]:
    """Split the Markdown report into sections by ## N. headers.

    Returns:
        List of HTML strings, one per section. If fewer than 6 sections
        are found, empty strings fill the remaining slots.
    """
    parts = SECTION_PATTERN.split(markdown_content)
    # First element is everything before the first ## N. header (usually empty)
    # Remaining elements are the section bodies (after the header text)
    section_bodies = []
    for part in parts[1:]:
        # The section title is on the first line, content follows
        lines = part.split("\n", 1)
        body = lines[1].strip() if len(lines) > 1 else ""
        section_bodies.append(_md_to_html(body))

    # Pad to 6 sections
    while len(section_bodies) < 6:
        section_bodies.append("<p>No data available.</p>")

    return section_bodies


def _md_to_html(md_content: str) -> str:
    """Convert a Markdown string to HTML using the markdown library."""
    return markdown.markdown(md_content, extensions=["tables"])


def _count_items(section_html: str) -> int:
    """Count table rows (excluding header) in a section to get the number of items."""
    # Count <tr> tags minus 1 for the header row
    rows = section_html.count("<tr>")
    return max(0, rows - 1) if rows > 0 else 0


def _build_html(repo_name: str, sections: list[str]) -> str:
    """Build the complete HTML document from parsed sections."""
    initial = repo_name[0].upper() if repo_name else "?"

    improvements_count = _count_items(sections[4])
    security_count = _count_items(sections[5])

    cards_html = ""
    for i, (section_id, title, content) in enumerate(
        zip(SECTION_IDS, SECTION_TITLES, sections)
    ):
        cards_html += f"""
  <section class="card" id="{section_id}">
    <h2><span class="section-num">{i + 1}</span> {title}</h2>
    {content}
  </section>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Analysis: {repo_name}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">

  <header class="report-header">
    <div class="repo-name">
      <div class="icon">{initial}</div>
      {repo_name}
    </div>
    <div class="repo-url">Analyzed by repo-analyzer</div>
  </header>

  <div class="metrics">
    <div class="metric">
      <div class="label">Security Issues</div>
      <div class="value red">{security_count}</div>
    </div>
    <div class="metric">
      <div class="label">Improvements</div>
      <div class="value amber">{improvements_count}</div>
    </div>
  </div>

{cards_html}
  <footer>Generated by repo-analyzer</footer>

</div>
</body>
</html>
"""
```

- [ ] **Step 2: Verify import and basic functionality**

```bash
cd /home/tfb/projects/repo-analyzer
source .venv/bin/activate
python -c "
from repo_analyzer.html_report import generate_html, get_stylesheet

# Test get_stylesheet
css = get_stylesheet()
assert len(css) > 100, 'CSS too short'
assert '.container' in css, 'Missing .container class'
print(f'CSS OK: {len(css)} chars')

# Test generate_html with minimal input
test_md = '''## 1. Project Summary
A test project.

## 2. Tech Stack
Python 3.11

## 3. Structure & Architecture
Simple flat structure.

## 4. Code Quality
Good quality.

## 5. Suggested Improvements (Top 5)
| # | What | Why | How |
|---|------|-----|-----|
| 1 | Add tests | Coverage | pytest |

## 6. Security Issues (Top 5)
| # | Issue | Severity | Recommendation |
|---|-------|----------|----------------|
| 1 | No auth | High | Add auth |
| 2 | No TLS | Medium | Add TLS |
'''

html = generate_html(test_md, 'test-repo')
assert '<!DOCTYPE html>' in html
assert 'test-repo' in html
assert 'Project Summary' in html
assert 'Security Issues' in html
assert '<table>' in html
print(f'HTML OK: {len(html)} chars')
print('All checks passed')
"
```

Expected: prints `CSS OK`, `HTML OK`, `All checks passed`.

- [ ] **Step 3: Commit**

```bash
git add src/repo_analyzer/html_report.py
git commit -m "feat: add html_report module with MD parser and HTML template"
```

---

### Task 4: Integrate HTML generation in main.py

**Files:**
- Modify: `repo-analyzer/src/repo_analyzer/main.py`

- [ ] **Step 1: Add import**

At the top of `main.py`, add the import after the existing imports (line 11):

```python
from .html_report import generate_html, get_stylesheet
```

The full import block becomes:

```python
from .analyzer import DEFAULT_MODEL, analyze
from .cloner import RepoCloner
from .collector import collect_context
from .html_report import generate_html, get_stylesheet
```

- [ ] **Step 2: Add HTML generation after MD write**

In the `main()` function, after the `output_path.write_text(report)` try/except block (after line 74), add the HTML generation. The section from line 69 to line 76 should become:

```python
            try:
                output_path.write_text(report)
            except OSError as e:
                print(f"Error: Could not write report to {output_path}: {e}", file=sys.stderr)
                print(report)
                sys.exit(1)

            html_path = output_path.with_suffix(".html")
            html_content = generate_html(report, repo_name)
            html_path.write_text(html_content)

            css_path = output_path.parent / "style.css"
            if not css_path.exists():
                css_path.write_text(get_stylesheet())

        print(f"Report saved to: {output_path}")
        print(f"HTML report: {html_path}")
```

- [ ] **Step 3: Verify CLI help still works**

```bash
cd /home/tfb/projects/repo-analyzer
source .venv/bin/activate
repo-analyzer --help
```

Expected: prints usage without errors.

- [ ] **Step 4: Commit**

```bash
git add src/repo_analyzer/main.py
git commit -m "feat: integrate HTML report generation into CLI pipeline"
```

---

### Task 5: End-to-End Test

**Files:** None (manual verification)

- [ ] **Step 1: Run against the nocode repo**

```bash
cd /home/tfb/projects/repo-analyzer
source .venv/bin/activate
repo-analyzer https://github.com/kelseyhightower/nocode
```

Expected output:
```
Cloning https://github.com/kelseyhightower/nocode...
Collecting repository context...
Collected 2 files (901 chars)
Analyzing with nvidia/nemotron-3-super-120b-a12b:free...
Report saved to: output/nocode-analysis.md
HTML report: output/nocode-analysis.html
```

- [ ] **Step 2: Verify output files exist**

```bash
ls -la output/
```

Expected: `nocode-analysis.md`, `nocode-analysis.html`, and `style.css` all exist.

- [ ] **Step 3: Verify HTML is valid**

```bash
head -5 output/nocode-analysis.html
```

Expected: starts with `<!DOCTYPE html>` and contains `<link rel="stylesheet" href="style.css">`.

- [ ] **Step 4: Open in browser and visually verify**

```bash
xdg-open output/nocode-analysis.html 2>/dev/null || echo "Open output/nocode-analysis.html in your browser"
```

Expected: page renders with Gradient Dark theme, header with repo name, metric cards, 6 sections in styled cards, footer.

- [ ] **Step 5: Include style.css in .gitignore exclusion**

The existing `.gitignore` has `output/*.md` and `!output/.gitkeep`. Add the HTML and CSS to the ignore list. Update `repo-analyzer/.gitignore`:

```
.env
.venv/
__pycache__/
*.egg-info/
output/*.md
output/*.html
output/style.css
!output/.gitkeep
```

- [ ] **Step 6: Commit**

```bash
git add .gitignore
git commit -m "chore: add HTML and CSS output to .gitignore"
```
