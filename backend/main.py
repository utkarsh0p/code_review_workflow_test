import os
import requests
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# GitHub token (PAT or GitHub App token)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN not set")

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

@app.post("/review")
async def review(request: Request):
    payload = await request.json()
    print("GITHUB PAYLOAD:", payload)

    repo = payload["repo"]            # owner/repo
    pr_number = int(payload["pr_number"])

    # 1️⃣ Fetch PR files (diffs)
    files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
    response = requests.get(files_url, headers=HEADERS)

    if response.status_code != 200:
        print("GitHub API ERROR:", response.text)
        raise HTTPException(status_code=500, detail="Failed to fetch PR files")

    files = response.json()

    review_summary = []
    print("\nPR DIFFS:")

    for f in files:
        if f.get("patch"):
            print("FILE:", f["filename"])
            print(f["patch"])
            print("------")

            review_summary.append(f"- `{f['filename']}` has changes")

    # 2️⃣ Build comment text
    if review_summary:
        comment_body = (
            "🤖 **Automated PR Review**\n\n"
            "I analyzed the following files:\n\n"
            + "\n".join(review_summary)
            + "\n\n✅ Review completed."
        )
    else:
        comment_body = "🤖 **Automated PR Review**\n\nNo code changes detected."

    # 3️⃣ Post comment on GitHub PR
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    comment_response = requests.post(
        comment_url,
        headers=HEADERS,
        json={"body": comment_body}
    )

    if comment_response.status_code != 201:
        print("Failed to post comment:", comment_response.text)
        raise HTTPException(status_code=500, detail="Failed to post PR comment")

    return {
        "msg": "Review completed and comment posted on PR"
    }

#check for the merge of the permissions