from github import GitHub
import requests

class StatsManager(GitHub):
    def __init__(self):
        super().__init__()

    def get_repo_stats(self, owner, repo):
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/stats/contributors", headers=self.headers)
        return response.json()
