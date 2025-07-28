import requests
import json
import httpx
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
google_api_key = os.getenv("GEMMA_TOKEN")

# Configure the Gemma API
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemma-7b-it')

async def get_pull_request_details(repo, pr_number, token=token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"token {token}"}
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

async def post_comment(repo, pr_number, comment, token=token):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    data = {"body": comment}
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
    with open('post_comment.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    return response.json()

def analyze_code(code):
    if not code:
        return "No code changes to analyze."
    
    try:
        prompt = """You are a code review assistant. Please analyze the following code changes and provide a brief, professional review.

        Code to analyze:
        {code}

        Please focus on:
        1. Key changes and their impact
        2. Potential issues or improvements
        3. Best practices and suggestions
        """
        
        response = model.generate_content(prompt.format(code=code))
        return response.text
    except Exception as e:
        return f"Error analyzing code: {str(e)}"





