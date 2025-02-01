from github import GitHub
import requests

class StatsManager(GitHub):
    def __init__(self):
        super().__init__()

    def get_repo_stats(self, owner, repo):
        """Obtiene las estadísticas de contribuyentes del repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/stats/contributors", headers=self.headers)
        return response.json()

    def get_repo_commits(self, owner, repo):
        """Obtiene los últimos commits del repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/commits", headers=self.headers)
        return response.json()

    def get_repo_branches(self, owner, repo):
        """Lista todas las ramas del repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/branches", headers=self.headers)
        return response.json()

    def get_repo_releases(self, owner, repo):
        """Obtiene las versiones (releases) del repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/releases", headers=self.headers)
        return response.json()

    def get_repo_issues(self, owner, repo):
        """Lista los issues abiertos en el repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/issues", headers=self.headers, params={"state": "open"})
        return response.json()

    def get_repo_pull_requests(self, owner, repo):
        """Lista los pull requests abiertos en el repositorio."""
        response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/pulls", headers=self.headers, params={"state": "open"})
        return response.json()

    def get_repo_overview(self, owner, repo):
        """Obtiene un resumen general del repositorio con estadísticas clave."""
        repo_info = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}", headers=self.headers).json()
        stats = {
            "Nombre": repo_info.get("name"),
            "Descripción": repo_info.get("description"),
            "Dueño": repo_info["owner"]["login"],
            "Privado": repo_info["private"],
            "Forks": repo_info.get("forks_count", 0),
            "Estrellas": repo_info.get("stargazers_count", 0),
            "Watchers": repo_info.get("watchers_count", 0),
            "Issues abiertos": repo_info.get("open_issues_count", 0),
            "Lenguaje principal": repo_info.get("language"),
        }
        return stats
