import requests
import json
import httpx
import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

token = os.getenv("GITHUB_TOKEN")
hf_token = os.getenv("HF_TOKEN") 

# Initialize the Inference Client
client = InferenceClient(
    provider="cerebras",
    api_key=hf_token,
)

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
    with open('tk.txt', 'a+') as file:
        file.write(f"Token3: {token}\n")
        file.write(f"url: {url}\n")
    print(url)
    print(headers)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
    with open('post_comment.json', 'w') as file:
        json.dump(response.json(), file, indent=4)
    return response.json()

def analyze_code(code):
    if not code:
        return "No code changes to analyze."
    
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",  
            messages=[
                {
                    "role": "system",
                    "content": "You are a code review assistant. Analyze the code changes and provide a brief, professional review."
                },
                {
                    "role": "user",
                    "content": f"Please analyze these code changes:\n\n{code}"
                }
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error analyzing code: {str(e)}"





