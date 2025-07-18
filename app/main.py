from fastapi import FastAPI
from fastapi import Request
import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from dotenv import load_dotenv
import os
import logging
import json

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, AI Code Review Assistant! This is testing3."}

@app.post("/webhook")
async def handle_webhook(request: Request):
    payload = await request.json()

    with open('webhook_payload.json', 'w') as json_file:
        json.dump(payload, json_file, indent=4)

    action = payload.get("action")
    pr_number = payload.get("number")
    repo = payload.get("repository", {}).get("full_name")

    if action == "opened":
        # Fetch PR details
        pr_details = get_pull_request_details(repo, pr_number, GITHUB_TOKEN)
        files = pr_details.get("files", [])

        # Analyze each file
        for file in files:
            code = file.get("patch")
            analysis = analyze_code(code)
            # Interpret analysis and create a comment
            comment = f"Analysis for {file.get('filename')}: {analysis}"
            post_comment(repo, pr_number, comment, GITHUB_TOKEN)

    return {"status": "processed"}

def get_pull_request_details(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"token {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def post_comment(repo, pr_number, comment, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    data = {"body": comment}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def analyze_code(code):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs