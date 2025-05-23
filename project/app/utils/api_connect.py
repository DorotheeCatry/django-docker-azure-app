from dotenv import load_dotenv, set_key
import os
import requests

ENV_FILE = ".env"

load_dotenv()

def get_api_token():
    token = os.getenv("API_TOKEN")

    login_data = {
        "username": os.getenv("API_USERNAME"),
        "password": os.getenv("API_PASSWORD")
    }

    api_base_url = os.getenv("API_BASE_URL")  # Correction ici
    if not api_base_url:
        raise ValueError("API_BASE_URL non défini dans le .env")

    response = requests.post(f"{api_base_url}/auth/login", json=login_data)

    if response.status_code == 200:
        token = response.json().get("access_token")

        if not token:
            raise Exception("Réponse API invalide : aucun access_token reçu")

        set_key(ENV_FILE, "API_TOKEN", token)
        load_dotenv()  # Recharge le .env pour que la variable soit utilisable immédiatement
        return token
    else:
        raise Exception(f"Échec de l'authentification ({response.status_code}): {response.text}")


