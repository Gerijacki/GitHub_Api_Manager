from src.Github import GitHub
import requests
from src.modules.Utils import *

class StatsManager(GitHub):
    def __init__(self):
        super().__init__()

    def get_repo_stats(self, owner, repo):
        """Obtiene las estadísticas de contribuyentes del repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/stats/contributors", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir les estadístiques: {e}")
            return None

    def get_repo_commits(self, owner, repo):
        """Obtiene los últimos commits del repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/commits", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir els commits: {e}")
            return []

    def get_repo_branches(self, owner, repo):
        """Lista todas las ramas del repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/branches", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir les branques: {e}")
            return []

    def get_repo_releases(self, owner, repo):
        """Obtiene las versiones (releases) del repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/releases", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir les releases: {e}")
            return []

    def get_repo_issues(self, owner, repo):
        """Lista los issues abiertos en el repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/issues", headers=self.headers, params={"state": "open"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir els issues oberts: {e}")
            return []

    def get_repo_pull_requests(self, owner, repo):
        """Lista los pull requests abiertos en el repositorio."""
        try:
            response = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}/pulls", headers=self.headers, params={"state": "open"})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir els pull requests: {e}")
            return []

    def get_repo_overview(self, owner, repo):
        """Obtiene un resumen general del repositorio con estadísticas clave."""
        try:
            repo_info = requests.get(f"{self.BASE_URL}/repos/{owner}/{repo}", headers=self.headers).json()
            if 'message' in repo_info:
                print_error(f"Repositori no trobat o error: {repo_info['message']}")
                return None

            stats = {
                "Nombre": repo_info.get("name", "Desconegut"),
                "Descripción": repo_info.get("description", "No disponible"),
                "Dueño": repo_info["owner"]["login"],
                "Privado": repo_info["private"],
                "Forks": repo_info.get("forks_count", 0),
                "Estrellas": repo_info.get("stargazers_count", 0),
                "Watchers": repo_info.get("watchers_count", 0),
                "Issues abiertos": repo_info.get("open_issues_count", 0),
                "Lenguaje principal": repo_info.get("language", "No disponible"),
            }
            return stats
        except requests.exceptions.RequestException as e:
            print_error(f"Error al obtenir el resum del repositori: {e}")
            return None
