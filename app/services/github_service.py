import requests
from transformers import AutoTokenizer, BertGenerationDecoder, BertGenerationConfig
import torch
import json
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("GITHUB_TOKEN")


tokenizer = AutoTokenizer.from_pretrained("google/bert_for_seq_generation_L-24_bbc_encoder")
config = BertGenerationConfig.from_pretrained("google/bert_for_seq_generation_L-24_bbc_encoder")
config.is_decoder = True
model = BertGenerationDecoder.from_pretrained(
    "google/bert_for_seq_generation_L-24_bbc_encoder", config=config
)
model.eval()

async def get_pull_request_details(repo, pr_number, token=token):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    headers = {"Authorization": f"token {token}"}
    with open('tk.txt', 'a+') as file:
        file.write(f"Token3: {token}\n")
        file.write(f"url: {url}\n")
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
    prompt = code + "Please analyze the code and provide a short explanation of the changes made."
    output_text = generate_from_prompt(prompt)
    return output_text

def generate_from_prompt(prompt, max_new_tokens=30):
    input_ids = tokenizer(prompt, return_token_type_ids=False, return_tensors="pt")["input_ids"]
    
    generated = input_ids.clone()
    
    for _ in range(max_new_tokens):
        with torch.no_grad():
            outputs = model(input_ids=generated)
            logits = outputs.logits
            next_token_logits = logits[:, -1, :]
            next_token_id = torch.argmax(next_token_logits, dim=-1).unsqueeze(-1)
        
        # If end-of-sentence token is generated, break
        if next_token_id.item() == tokenizer.eos_token_id:
            break
        
        generated = torch.cat((generated, next_token_id), dim=1)

    return tokenizer.decode(generated[0], skip_special_tokens=True)





