from dotenv import load_dotenv, set_key
import os
import requests

def get_api_token():
    login_data = {
        "username": os.getenv("API_USERNAME"),
        "password": os.getenv("API_PASSWORD")
    }

    api_base_url = os.getenv("API_BASE_URL")
    if not api_base_url:
        raise ValueError("API_BASE_URL not defined in the .env file")

    response = requests.post(f"{api_base_url}/auth/login", json=login_data)

    if response.status_code == 200:
        token = response.json().get("access_token")

        if not token:
            raise Exception("Invalid API response: no access_token received")

        os.environ["API_TOKEN"] = token
        return token
    else:
        raise Exception(f"Authentication failed ({response.status_code}): {response.text}")
