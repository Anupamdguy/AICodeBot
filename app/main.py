from fastapi import FastAPI
from fastapi import Request
from dotenv import load_dotenv
import os
import json
from .services.github_service import get_pull_request_details, post_comment, analyze_code


load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
with open('output_tk.txt', 'a+') as file:
    file.write(f"Token1: {GITHUB_TOKEN}\n")
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, AI Code Review Assistant! This is testing3."}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()
    with open('output_tk.txt', 'a+') as file:
        file.write(f"Token2: {GITHUB_TOKEN}\n")
    
    # Debugging: Log the entire payload
    with open('payload_debug.json', 'w') as debug_file:
        json.dump(payload, debug_file, indent=4)

    action = payload.get("action")
    pr_number = payload.get("number")
    repo = payload.get("repository", {}).get("full_name")

    if action == "opened":
        # Fetch PR details'
        pr_details = await get_pull_request_details(repo, pr_number, GITHUB_TOKEN)
        
        # Debugging: Log the PR details
        with open('pr_details_debug.json', 'w') as debug_file:
            json.dump(pr_details, debug_file, indent=4)

        files = pr_details.get("files", [])
        # Analyze each file
        for file in files:
            code = file.get("patch")
            analysis = analyze_code(code)
            comment = f"Analysis for {file.get('filename')}: {analysis}"
            await post_comment(repo, pr_number, comment, GITHUB_TOKEN)
            with open('output4.txt', 'w') as file:
                file.write(f"Files: {files}\n")

    if action == "synchronize":
        # Fetch PR details'
        pr_details = await get_pull_request_details(repo, pr_number, GITHUB_TOKEN)
        with open('output_tk.txt', 'a+') as file:
            file.write(f"Token3: {GITHUB_TOKEN}\n")
        # Debugging: Log the PR details
        with open('pr_details_debug.json', 'w') as debug_file:
            json.dump(pr_details, debug_file, indent=4)

        files = pr_details.get("files", [])

        # Analyze each file
        for file in files:
            # code = file.get("patch")
            # analysis = analyze_code(code)
            # comment = f"Analysis for {file.get('filename')}: {analysis}"
            comment = "testing from the code"
            await post_comment(repo, pr_number, comment, GITHUB_TOKEN)
            with open('output5.txt', 'w') as file:
                file.write(f"Comment: {comment}\n")

    return {"status": "processed"}