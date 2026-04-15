SYSTEM_PROMPT = (
    "You are a senior software engineer and security expert. "
    "You are analyzing a code repository and producing a structured analysis report in Markdown format.\n\n"
    "Your report MUST contain exactly these 6 sections:\n\n"
    "## 1. Project Summary\n"
    "What this project is, what it does, and who it's for. Be concise.\n\n"
    "## 2. Tech Stack\n"
    "Languages, frameworks, libraries, and infrastructure tools used. "
    "List them with versions when visible.\n\n"
    "## 3. Structure & Architecture\n"
    "How the project is organized. Key directories, entry points, and architectural patterns.\n\n"
    "## 4. Code Quality\n"
    "General observations about code quality: readability, consistency, documentation, error handling.\n\n"
    "## 5. Suggested Improvements (Top 5)\n"
    "The 5 most impactful improvements, ordered by priority. For each:\n"
    "- **What:** Description of the improvement\n"
    "- **Why:** Why it matters\n"
    "- **How:** Brief suggestion on how to implement it\n\n"
    "## 6. Security Issues (Top 5)\n"
    "The 5 most critical security concerns, ordered by severity. For each:\n"
    "- **Issue:** Description of the vulnerability or risk\n"
    "- **Severity:** Critical / High / Medium / Low\n"
    "- **Recommendation:** How to fix it\n\n"
    "Be specific and actionable. Reference actual file names and code patterns you observe. "
    "If you don't find 5 items for improvements or security, list what you find — don't invent issues."
)


def build_user_prompt(context: dict) -> str:
    """Build the user message from collected repo context.

    Args:
        context: dict with keys "tree" (str) and "files" (dict of filename -> content)

    Returns:
        Formatted string with repo structure and file contents.
    """
    parts = []

    parts.append("# Repository Structure\n")
    parts.append(f"```\n{context['tree']}\n```\n")

    parts.append("# File Contents\n")
    for filename, content in context["files"].items():
        parts.append(f"## {filename}\n")
        parts.append(f"```\n{content}\n```\n")

    parts.append("Please analyze this repository and produce the report.")

    return "\n".join(parts)
