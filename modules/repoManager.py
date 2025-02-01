from github import GitHub
import requests

class RepoManager(GitHub):
    def __init__(self):
        super().__init__()

    def create_repo(self, repo_name, private=True, description="", add_readme=False, add_license=False):
        """Crea un nou repo de GitHub."""
        url = f"{self.BASE_URL}/user/repos"
        
        data = {
            "name": repo_name,
            "private": private,
            "description": description,
        }

        if add_readme:
            data["has_issues"] = True
        if add_license:
            data["license_template"] = "mit"

        response = requests.post(url, headers=self.headers, json=data)
        
        return response.json()

    def delete_repo(self, repo_name):
        """Elimina un repo de GitHub."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204

    def create_branch(self, repo_name, new_branch, base_branch="main"):
        """Crea una nova branch."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs/heads/{base_branch}"
        base_branch_data = requests.get(url, headers=self.headers).json()

        if "object" not in base_branch_data:
            return {"error": "La branca base no existeix."}

        sha = base_branch_data["object"]["sha"]
        new_branch_url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs"
        data = {
            "ref": f"refs/heads/{new_branch}",
            "sha": sha
        }
        response = requests.post(new_branch_url, headers=self.headers, json=data)
        return response.json()

    def delete_branch(self, repo_name, branch_name):
        """Elimina una branch d'un repo."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs/heads/{branch_name}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 204

    def merge_branches(self, repo_name, base, head):
        """Fusiona (merge) dos branch."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/merges"
        data = {
            "base": base,
            "head": head,
            "commit_message": f"Merge {head} into {base}"
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def create_pull_request(self, repo_name, title, head, base="main", body=""):
        """Genera una pull request."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls"
        data = {
            "title": title,
            "head": head,
            "base": base,
            "body": body
        }
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()

    def list_pull_requests(self, repo_name, state="open"):
        """Llista les pull request obertes."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls"
        response = requests.get(url, headers=self.headers, params={"state": state})
        return response.json()

    def merge_pull_request(self, repo_name, pr_number):
        """Fusiona (merge) una pull request."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls/{pr_number}/merge"
        response = requests.put(url, headers=self.headers)
        return response.json()

    def close_pull_request(self, repo_name, pr_number):
        """Tanca una pull request sense fer merge"""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls/{pr_number}"
        data = {"state": "closed"}
        response = requests.patch(url, headers=self.headers, json=data)
        return response.json()

    def add_collaborator(self, repo_name, collaborator, permission="push"):
        """Afegeix un col·laborador amb permisos concrets."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/collaborators/{collaborator}"
        data = {"permission": permission}
        response = requests.put(url, headers=self.headers, json=data)
        return response.status_code == 201

    def list_collaborators(self, repo_name):
        """Lista els col·laboradors d'un repo."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/collaborators"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def set_collaborator_permissions(self, repo_name, collaborator, permission):
        """Modifica els permisos d'un col·laborador dins d'un repo."""
        return self.add_collaborator(repo_name, collaborator, permission)
