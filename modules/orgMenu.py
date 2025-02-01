import os
# ================== GESTIÓN DE ORGANIZACIONES ================== #
class OrgMenu:
    def __init__(self, org_manager):
        self.org_manager = org_manager
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("Prem Enter per continuar...")

def gestionar_organizaciones(self):
    while True:
        self.clear_screen()
        print("\n==== GESTIÓ DE LES ORGANITZACIÓNS ====")
        print("1. Llistar les meves orgs")
        print("2. Veure detalls d'una org")
        print("3. Llistar membres d'una org")
        print("4. Afegir membre a la org")
        print("5. Eliminar membre d'una org")
        print("6. Llistar repos d'una org")
        print("7. Crear repo en una org")
        print("8. Tornar al menú principal")

        opcion = input("\nSel·lecciona una opció: ")

        if opcion == "1":
            self.listar_orgs()
        elif opcion == "2":
            self.ver_detalles_org()
        elif opcion == "3":
            self.listar_miembros_org()
        elif opcion == "4":
            self.agregar_miembro_org()
        elif opcion == "5":
            self.eliminar_miembro_org()
        elif opcion == "6":
            self.listar_repos_org()
        elif opcion == "7":
            self.crear_repo_org()
        elif opcion == "8":
            break
        else:
            print("\nOpció no vàlida.")

        self.pause()

def listar_orgs(self):
    orgs = self.org_manager.list_orgs()
    print("\n=== LES MEVES ORGS ===")
    for org in orgs:
        print(f"- {org['login']}")

def ver_detalles_org(self):
    org_name = input("Nom de l'org: ")
    details = self.org_manager.get_org_details(org_name)

    if not details:
        print("❌ No s'ha trobat informació.")
        return

    print("\n=== Detalls de l'org ===")
    print(f"📌 Nom: {details.get('name', 'NA')}")
    print(f"🔗 URL GITHUB: {details.get('html_url', 'NA')}")
    print(f"📍 Ubicació: {details.get('location', 'NA')}")
    print(f"📧 Email: {details.get('email', 'NA')}")
    print(f"📅 Creada el: {details.get('created_at', 'NA')}")
    print(f"📅 Última actualizació: {details.get('updated_at', 'NA')}")
    print(f"📝 Descripció: {details.get('description', 'NA')}")
    print(f"🐦 Twitter: {details.get('twitter_username', 'NA')}")
    print(f"🖥 Blog: {details.get('blog', 'NA')}")

    print("\n=== 📊 Estadístiques ===")
    print(f"📂 Repos públics: {details.get('public_repos', 0)}")
    print(f"🔒 Repos privats: {details.get('total_private_repos', 0)}")
    print(f"⭐ Stars: {details.get('followers', 0)}")
    print(f"📌 Seguits: {details.get('following', 0)}")
    print(f"👥 Col·laboradors: {details.get('collaborators', 0)}")

    print("\n=== 🔐 Configuració dels Repos ===")
    print(
        f"📦 Membres poden crear repos: {'Sí' if details.get('members_can_create_repositories', False) else 'No'}"
    )
    print(
        f"📢 Membres poden crear repos públics: {'Sí' if details.get('members_can_create_public_repositories', False) else 'No'}"
    )
    print(
        f"🔒 Membres poden crear repos privats: {'Sí' if details.get('members_can_create_private_repositories', False) else 'No'}"
    )

    print("\n🖼 Avatar:")
    print(details.get("avatar_url", "NA"))

def listar_miembros_org(self):
    org_name = input("Nom de l'org: ")
    members = self.org_manager.list_org_members(org_name)
    print("\n=== Membres de l'org ===")
    for member in members:
        print(f"- {member['login']}")

def agregar_miembro_org(self):
    org_name = input("Nom de l'org: ")
    username = input("Usuari a afegir: ")
    role = input("Rol (member/admin): ")
    response = self.org_manager.add_member_to_org(org_name, username, role)
    print(response)

def eliminar_miembro_org(self):
    org_name = input("Nom de l'org: ")
    username = input("Usuari a eliminar: ")
    if self.org_manager.remove_member_from_org(org_name, username):
        print("✅ Usuario eliminat correctament.")
    else:
        print("❌ Error en eliminar l'usuari.")

def listar_repos_org(self):
    org_name = input("Nom de l'org: ")
    repos = self.org_manager.list_org_repos(org_name)
    print("\n=== Repos de l'org ===")
    for repo in repos:
        print(f"- {repo['name']} ({'Privat' if repo['private'] else 'Públic'})")

def crear_repo_org(self):
    org_name = input("Nom de l'org: ")
    repo_name = input("Nom del nou repo: ")
    privado = input("Privat? (s/n): ").lower() == "s"
    response = self.org_manager.create_org_repo(org_name, repo_name, privado)
    print(response)