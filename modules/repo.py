from github import GitHub
import requests

class RepoManager(GitHub):
    def __init__(self):
        super().__init__()

    def delete_repo(self, repo_name):
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204
