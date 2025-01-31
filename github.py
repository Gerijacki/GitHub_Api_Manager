import requests
from config import GITHUB_TOKEN

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

    def list_repos(self):
        response = requests.get(f"{self.BASE_URL}/user/repos", headers=self.headers)
        return response.json()

    def create_repo(self, name, private=True):
        data = {"name": name, "private": private}
        response = requests.post(f"{self.BASE_URL}/user/repos", json=data, headers=self.headers)
        return response.json()
