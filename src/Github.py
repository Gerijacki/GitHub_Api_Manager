import requests
from src.config import GITHUB_TOKEN

class GitHub:
    BASE_URL = "https://api.github.com"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }

    def get_user(self):
        response = requests.get(f"{self.BASE_URL}/user", headers=self.headers)
        return response.json()

