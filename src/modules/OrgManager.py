from src.Github import GitHub
import requests

class OrgManager(GitHub):
    def __init__(self):
        super().__init__()

    def list_orgs(self):
        """Llista totes les orgs de l'usuari."""
        try:
            response = requests.get(f"{self.BASE_URL}/user/orgs", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al llistar organitzacions: {str(e)}")
            return []

    def get_org_details(self, org_name):
        """Obte detalls d'una org en concret."""
        try:
            response = requests.get(f"{self.BASE_URL}/orgs/{org_name}", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtenir detalls de l'org {org_name}: {str(e)}")
            return {}

    def list_org_members(self, org_name):
        """Llista membres d'una org"""
        try:
            response = requests.get(f"{self.BASE_URL}/orgs/{org_name}/members", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al llistar membres de l'org {org_name}: {str(e)}")
            return []

    def add_member_to_org(self, org_name, username, role="member"):
        """
        Afageix un membre a la org amb rol (member o admin)
        """
        if role not in ["member", "admin"]:
            print("Rol invàlid. Ha de ser 'member' o 'admin'.")
            return {}

        try:
            data = {"role": role}
            response = requests.put(f"{self.BASE_URL}/orgs/{org_name}/memberships/{username}", json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al afegir el membre {username} a l'org {org_name}: {str(e)}")
            return {}

    def remove_member_from_org(self, org_name, username):
        """Elimina usuari d'una org."""
        try:
            response = requests.delete(f"{self.BASE_URL}/orgs/{org_name}/memberships/{username}", headers=self.headers)
            response.raise_for_status()
            if response.status_code == 204:
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error al eliminar el membre {username} de l'org {org_name}: {str(e)}")
            return False

    def list_org_repos(self, org_name):
        """Llista repos d'una org"""
        try:
            response = requests.get(f"{self.BASE_URL}/orgs/{org_name}/repos", headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al llistar repositoris de l'org {org_name}: {str(e)}")
            return []

    def create_org_repo(self, org_name, repo_name, private=True, create_readme=False, create_privacy_policy=False, create_terms_of_service=False):
        """Crea un repositori per una organització"""
        if not repo_name.strip():
            print("El nom del repositori no pot estar buit.")
            return {}

        data = {
            "name": repo_name,
            "private": private,
            "auto_init": create_readme,
        }
        if create_privacy_policy:
            data["license_template"] = "mit"
            
        if create_terms_of_service:
            data["has_issues"] = True

        try:
            response = requests.post(f"{self.BASE_URL}/orgs/{org_name}/repos", json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al crear el repositori {repo_name} a l'org {org_name}: {str(e)}")
            return {}
