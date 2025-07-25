import requests
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import json
import httpx


model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased")
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


async def get_pull_request_details(repo, pr_number, token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"Bearer {token}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        pr_details = response.json()

        # Fetch files changed in the pull request
        files_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/files"
        files_response = await client.get(files_url, headers=headers)
        files = files_response.json()

    # Add files to the pull request details
    pr_details['files'] = files
    with open('pr_details.json', 'w') as file:
        json.dump(pr_details, file, indent=4)
    return pr_details


async def post_comment(repo, pr_number, comment, token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"body": comment}
    print(url)
    print(headers)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
    with open('post_comment.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    return response.json()


def analyze_code(code):
    inputs = tokenizer(code, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)
    return outputs 