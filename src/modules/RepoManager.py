from src.Github import GitHub
import requests

class RepoManager(GitHub):
    def __init__(self):
        super().__init__()
    
    def _handle_request(self, method, url, **kwargs):
        """Gestor d'errors genèric per a peticions HTTP."""
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error en la petició: {str(e)}"}
        except ValueError:
            return {"error": "Resposta inesperada del servidor."}
    
    def create_repo(self, repo_name, private=True, description="", add_readme=False, add_license=False):
        """Crea un nou repositori de GitHub."""
        url = f"{self.BASE_URL}/user/repos"
        data = {"name": repo_name, "private": private, "description": description}
        if add_readme:
            data["has_issues"] = True
        if add_license:
            data["license_template"] = "mit"
        return self._handle_request("POST", url, json=data)
    
    def delete_repo(self, repo_name):
        """Elimina un repositori de GitHub."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}"
        response = self._handle_request("DELETE", url)
        return response.get("message") == "Not Found" or response == {}

    def create_branch(self, repo_name, new_branch, base_branch="main"):
        """Crea una nova branca."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs/heads/{base_branch}"
        base_branch_data = self._handle_request("GET", url)
        
        if "object" not in base_branch_data:
            return {"error": "La branca base no existeix."}
        
        sha = base_branch_data["object"]["sha"]
        new_branch_url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs"
        data = {"ref": f"refs/heads/{new_branch}", "sha": sha}
        return self._handle_request("POST", new_branch_url, json=data)
    
    def delete_branch(self, repo_name, branch_name):
        """Elimina una branca."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/git/refs/heads/{branch_name}"
        response = self._handle_request("DELETE", url)
        return response.get("message") == "Not Found" or response == {}
    
    def merge_branches(self, repo_name, base, head):
        """Fusiona dues branques."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/merges"
        data = {"base": base, "head": head, "commit_message": f"Merge {head} into {base}"}
        return self._handle_request("POST", url, json=data)
    
    def create_pull_request(self, repo_name, title, head, base="main", body=""):
        """Crea una nova pull request."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls"
        data = {"title": title, "head": head, "base": base, "body": body}
        return self._handle_request("POST", url, json=data)
    
    def list_pull_requests(self, repo_name, state="open"):
        """Llista les pull requests."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls"
        return self._handle_request("GET", url, params={"state": state})
    
    def merge_pull_request(self, repo_name, pr_number):
        """Fusiona una pull request."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls/{pr_number}/merge"
        return self._handle_request("PUT", url)
    
    def close_pull_request(self, repo_name, pr_number):
        """Tanca una pull request."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/pulls/{pr_number}"
        data = {"state": "closed"}
        return self._handle_request("PATCH", url, json=data)
    
    def add_collaborator(self, repo_name, collaborator, permission="push"):
        """Afegeix un col·laborador."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/collaborators/{collaborator}"
        data = {"permission": permission}
        response = self._handle_request("PUT", url, json=data)
        return "message" not in response
    
    def list_collaborators(self, repo_name):
        """Llista els col·laboradors d'un repositori."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/collaborators"
        return self._handle_request("GET", url)
    
    def list_branches(self, repo_name):
        """Llista les branques d'un repositori."""
        username = self.get_user().get("login", "")
        url = f"{self.BASE_URL}/repos/{username}/{repo_name}/branches"
        return self._handle_request("GET", url)
    
    def list_repos(self):
        """Llista només els repositoris on l'usuari autenticat és propietari o col·laborador amb permisos d'edició"""
        url = f"{self.BASE_URL}/user/repos"
        params = {
            "per_page": 100,
            "affiliation": "owner,collaborator"
        }
        return self._handle_request("GET", url, params=params)



