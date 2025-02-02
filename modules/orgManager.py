from github import GitHub
import requests

class OrgManager(GitHub):
    def __init__(self):
        super().__init__()

    def list_orgs(self):
        """Lista todas las organizaciones a las que pertenece el usuario autenticado."""
        response = requests.get(f"{self.BASE_URL}/user/orgs", headers=self.headers)
        return response.json()

    def get_org_details(self, org_name):
        """Obtiene los detalles de una organización específica."""
        response = requests.get(f"{self.BASE_URL}/orgs/{org_name}", headers=self.headers)
        return response.json()

    def list_org_members(self, org_name):
        """Lista todos los miembros de una organización."""
        response = requests.get(f"{self.BASE_URL}/orgs/{org_name}/members", headers=self.headers)
        return response.json()

    def add_member_to_org(self, org_name, username, role="member"):
        """
        Añade un usuario a la organización.
        - role puede ser 'member' o 'admin'
        """
        data = {"role": role}
        response = requests.put(f"{self.BASE_URL}/orgs/{org_name}/memberships/{username}", json=data, headers=self.headers)
        return response.json()

    def remove_member_from_org(self, org_name, username):
        """Elimina un usuario de la organización."""
        response = requests.delete(f"{self.BASE_URL}/orgs/{org_name}/memberships/{username}", headers=self.headers)
        return response.status_code == 204  # True vs false

    def list_org_repos(self, org_name):
        """Lista los repositorios de una organización."""
        response = requests.get(f"{self.BASE_URL}/orgs/{org_name}/repos", headers=self.headers)
        return response.json()

    def create_org_repo(self, org_name, repo_name, private=True, create_readme=False, create_privacy_policy=False, create_terms_of_service=False):
        """Crea un nou repositori en l'organització amb fitxers opcionals."""
        data = {
            "name": repo_name,
            "private": private,
            "auto_init": create_readme, 
        }
        if create_privacy_policy:
            data["license_template"] = "mit"
            
        if create_terms_of_service:
            data["has_issues"] = True

        response = requests.post(f"{self.BASE_URL}/orgs/{org_name}/repos", json=data, headers=self.headers)
        return response.json()
