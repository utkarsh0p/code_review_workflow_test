import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException

from parse_diff import parse_diff
from context_builder import build_context

# LOAD .env FIRST
load_dotenv()

app = FastAPI()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}


@app.post("/review")
async def review(request: Request):
    payload = await request.json()

    repo = payload["repo"]
    pr_number = int(payload["pr_number"])

    # 1️⃣ Fetch PR files
    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(files_url, headers=HEADERS, timeout=20)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch PR files")

    files = response.json()

    # 2️⃣ Parse diffs
    file_changes = []
    for f in files:
        if f.get("patch"):
            parsed = parse_diff(f["patch"])
            if parsed:
                file_changes.append({
                    "file": f["filename"],
                    "changes": parsed
                })

    # 3️⃣ Build repo context (README etc.)
    context = build_context(repo, HEADERS)

    # 4️⃣ FINAL LLM INPUT (DO NOT CALL LLM YET)
    llm_input = {
        "repo": repo,
        "pull_request": {
            "number": pr_number,
            "title": payload.get("title", "")
        },
        "context": context,
        "changes": file_changes,
        "review_rules": {
            "focus": ["bugs", "logic errors", "security"],
            "ignore": ["formatting", "style", "comments"],
            "max_comments": 5
        }
    }

    # Debug output
    print("===== LLM INPUT =====")
    print(llm_input)

    return {
        "msg": "ok",
        "llm_input": llm_input
    }
#test line