import argparse
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

from .analyzer import DEFAULT_MODEL, analyze
from .cloner import RepoCloner
from .collector import collect_context
from .html_report import generate_html, get_stylesheet


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze a GitHub repository and generate a Markdown report.",
    )
    parser.add_argument(
        "url",
        help="GitHub repository URL (e.g. https://github.com/user/repo)",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (default: output/<repo-name>-analysis.md)",
    )
    parser.add_argument(
        "-m", "--model",
        default=DEFAULT_MODEL,
        help=f"OpenRouter model to use (default: {DEFAULT_MODEL})",
    )
    return parser.parse_args()


def extract_repo_name(url: str) -> str:
    """Extract 'repo' from a GitHub URL like https://github.com/user/repo."""
    match = re.search(r"github\.com/[^/]+/([^/.]+)", url)
    if not match:
        print(f"Error: Could not parse repo name from URL: {url}")
        sys.exit(1)
    return match.group(1)


def main():
    load_dotenv()
    args = parse_args()

    if not os.environ.get("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not set.")
        print("Create a .env file with: OPENROUTER_API_KEY=your-key-here")
        sys.exit(1)

    repo_name = extract_repo_name(args.url)

    output_path = Path(args.output) if args.output else Path(f"output/{repo_name}-analysis.md")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Cloning {args.url}...")
    try:
        with RepoCloner(args.url) as repo_path:
            print("Collecting repository context...")
            context = collect_context(repo_path)

            file_count = len(context["files"])
            total_chars = len(context["tree"]) + sum(len(v) for v in context["files"].values())
            print(f"Collected {file_count} files ({total_chars} chars)")

            print(f"Analyzing with {args.model}...")
            report = analyze(context, args.model)
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
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
