import requests

# Define the base URL for the API
base_url = "http://127.0.0.1:8000"

# Function to test GET request
def test_get_root():
    response = requests.get(f"{base_url}/")
    print("GET / response:", response.json())

# Function to test POST request
def test_post_webhook():
    # Example payload for the webhook
    payload = {
        "action": "opened",
        "number": 1,
        "repository": {
            "full_name": "user/repo"
        }
    }
    response = requests.post(f"{base_url}/webhook", json=payload)
    print("POST /webhook response:", response.json())

if __name__ == "__main__":
    test_get_root()
    test_post_webhook()