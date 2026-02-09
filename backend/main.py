import os
from dotenv import load_dotenv
import requests
from fastapi import FastAPI, Request, HTTPException

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

    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(files_url, headers=HEADERS, timeout=20)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch PR files")

    files = response.json()

    # ✅ LLM-friendly structure
    # Each item has: file name + its related diff
    file_changes = []

    for f in files:
        if f.get("patch"):
            file_changes.append({
                "file": f["filename"],
                "diff": f["patch"]
            })

    # Summary (only file names)
    review_summary = [
        f"- `{item['file']}` has changes"
        for item in file_changes
    ]

    # GitHub PR comment (summary only)
    comment_body = (
        "🤖 **Automated PR Review**\n\n"
        "hi from utkarsh 👋\n\n"
        + "\n".join(review_summary)
        + "\n\n✅ Review completed."
    )

    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(
        comment_url,
        headers=HEADERS,
        json={"body": comment_body},
        timeout=20
    )

    # Debug logs (see structure clearly)
    print("FILE CHANGES (LLM READY):")
    for item in file_changes:
        print("FILE:", item["file"])
        print(item["diff"])
        print("-" * 40)

    return {
        "msg": "ok",
        "file_changes": file_changes
    }

#line in branch2 for testing merge
#line in branch2 for test merge
#line branch2 for test merge again
#checking for the pr message from the backend
