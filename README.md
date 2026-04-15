# repo-analyzer

AI agent that analyzes GitHub repositories and generates a structured Markdown report with project summary, tech stack analysis, improvement suggestions, and security findings.

## Setup

1. Create a virtual environment and install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

2. Create a `.env` file with your OpenRouter API key:

```bash
cp .env.example .env
# Edit .env and add your key
```

Get your API key at https://openrouter.ai/keys

## Usage

```bash
# Basic usage
repo-analyzer https://github.com/user/repo

# Custom model
repo-analyzer https://github.com/user/repo -m google/gemini-2.5-flash

# Custom output path
repo-analyzer https://github.com/user/repo -o my-report.md
```

## What It Does

1. Clones the repository (shallow clone)
2. Collects context: file tree, config files, entry points, code samples
3. Sends context to an LLM via OpenRouter
4. Generates a Markdown report with:
   - Project Summary
   - Tech Stack
   - Structure & Architecture
   - Code Quality
   - Suggested Improvements (Top 5)
   - Security Issues (Top 5)
