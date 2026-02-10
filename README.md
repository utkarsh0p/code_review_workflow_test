# Context-Aware GitHub PR Reviewer

This project is an automated GitHub Pull Request reviewer that gives **only high-value comments**.

It understands the **repository context** and avoids noisy, generic AI feedback.

---

## What This Project Does

When a Pull Request is opened or updated:

1. GitHub sends a webhook
2. FastAPI backend receives the event
3. Only the **changed code** is analyzed
4. Repository context is read (README, rules, structure)
5. AI reviews the code
6. **Limited inline comments** are posted on the PR

---

## Why This Exists

Most AI code reviewers:
- Comment on everything
- Give generic advice
- Create noise in PRs

This reviewer:
- Focuses on **bugs, logic, and security**
- Ignores formatting and style
- Uses a **strict comment budget** (max 3–5 comments)

---

## Key Features

- Repo-aware (reads README and rules)
- Reviews only changed lines
- Inline GitHub PR comments
- Comment budget to avoid spam
- Fully automated via GitHub Actions

---

## Tech Stack

- Python
- FastAPI
- GitHub Webhooks
- GitHub REST API
- GitHub Actions
- LLM (OpenAI / Claude / Gemini)

Libraries:
- requests
- uvicorn
- python-dotenv

---


---

## How It Works

- GitHub Action triggers on PR
- Webhook sends PR info to backend
- Backend fetches changed files
- Only `+` and `-` lines are reviewed
- Repo rules are added as context
- AI finds high-risk issues
- Max 3–5 comments are posted

---

## Comment Budget

- Max comments per PR: 3–5
- Priority:
  - Bugs
  - Security issues
  - Logic errors
- Ignored:
  - Formatting
  - Style
  - Minor suggestions

---

## Setup

```bash
pip install -r requirements.txt


