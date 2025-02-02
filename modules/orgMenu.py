from modules.utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info
# ================== GESTIÓN DE ORGANIZACIONES ================== #
class OrgMenu:
    def __init__(self, org_manager):
        self.org_manager = org_manager

def gestionar_organizaciones(self):
    while True:
        clear_screen()
        print_info("\n==== GESTIÓ DE LES ORGANITZACIÓNS ====")
        print_info("1. Llistar les meves orgs")
        print_info("2. Veure detalls d'una org")
        print_info("3. Llistar membres d'una org")
        print_info("4. Afegir membre a la org")
        print_info("5. Eliminar membre d'una org")
        print_info("6. Llistar repos d'una org")
        print_info("7. Crear repo en una org")
        print_info("8. Tornar al menú principal")

        opcion = input_info("\nSel·lecciona una opció: ")

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
            print_error("\nOpció no vàlida.")

        pause()

def listar_orgs(self):
    orgs = self.org_manager.list_orgs()
    print_info("\n=== LES MEVES ORGS ===")
    for org in orgs:
        print_info(f"- {org['login']}")

def ver_detalles_org(self):
    org_name = input_info("Nom de l'org: ")
    details = self.org_manager.get_org_details(org_name)

    if not details:
        print_error("No s'ha trobat informació.")
        return

    print_info("\n=== Detalls de l'org ===")
    print_info(f"📌 Nom: {details.get('name', 'NA')}")
    print_info(f"🔗 URL GITHUB: {details.get('html_url', 'NA')}")
    print_info(f"📍 Ubicació: {details.get('location', 'NA')}")
    print_info(f"📧 Email: {details.get('email', 'NA')}")
    print_info(f"📅 Creada el: {details.get('created_at', 'NA')}")
    print_info(f"📅 Última actualizació: {details.get('updated_at', 'NA')}")
    print_info(f"📝 Descripció: {details.get('description', 'NA')}")
    print_info(f"🐦 Twitter: {details.get('twitter_username', 'NA')}")
    print_info(f"🖥 Blog: {details.get('blog', 'NA')}")

    print_info("\n=== 📊 Estadístiques ===")
    print_info(f"📂 Repos públics: {details.get('public_repos', 0)}")
    print_info(f"🔒 Repos privats: {details.get('total_private_repos', 0)}")
    print_info(f"⭐ Stars: {details.get('followers', 0)}")
    print_info(f"📌 Seguits: {details.get('following', 0)}")
    print_info(f"👥 Col·laboradors: {details.get('collaborators', 0)}")

    print_info("\n=== 🔐 Configuració dels Repos ===")
    print_info(
        f"📦 Membres poden crear repos: {'Sí' if details.get('members_can_create_repositories', False) else 'No'}"
    )
    print_info(
        f"📢 Membres poden crear repos públics: {'Sí' if details.get('members_can_create_public_repositories', False) else 'No'}"
    )
    print_info(
        f"🔒 Membres poden crear repos privats: {'Sí' if details.get('members_can_create_private_repositories', False) else 'No'}"
    )

    print_info("\n🖼 Avatar:")
    print_info(details.get("avatar_url", "NA"))

def listar_miembros_org(self):
    org_name = input_info("Nom de l'org: ")
    members = self.org_manager.list_org_members(org_name)
    print_info("\n=== Membres de l'org ===")
    for member in members:
        print_info(f"- {member['login']}")

def agregar_miembro_org(self):
    org_name = input_info("Nom de l'org: ")
    username = input_info("Usuari a afegir: ")
    role = input_info("Rol (member/admin): ")
    response = self.org_manager.add_member_to_org(org_name, username, role)
    print_info(response)

def eliminar_miembro_org(self):
    org_name = input_info("Nom de l'org: ")
    username = input_info("Usuari a eliminar: ")
    confirm = input_warning(f"Estàs segur que vols eliminar l'usuari {username} de l'organització {org_name}? (s/n)")
    if (confirm.lower == "s"):
        if self.org_manager.remove_member_from_org(org_name, username):
            print_success("Usuario eliminat correctament.")
        else:
            print_error("Error en eliminar l'usuari.")
    else:
        print_warning("Acció denegada")

def listar_repos_org(self):
    org_name = input_info("Nom de l'org: ")
    repos = self.org_manager.list_org_repos(org_name)
    print_info("\n=== Repos de l'org ===")
    for repo in repos:
        print_info(f"- {repo['name']} ({'Privat' if repo['private'] else 'Públic'})")

def crear_repo_org(self):
    org_name = input_info("Nom de l'org: ")
    repo_name = input_info("Nom del nou repo: ")
    privado = input_info("Privat? (s/n): ").lower() == "s"
    crear_readme = input_info("Vols incloure un README al repositori? (s/n): ").lower() == "s"
    crear_privacy_policy = input_info("Vols incloure la política de privacitat? (s/n): ").lower() == "s"
    crear_terms_of_service = input_info("Vols incloure la política d'usos? (s/n): ").lower() == "s"

    response = self.org_manager.create_org_repo(org_name, repo_name, privado, crear_readme, crear_privacy_policy, crear_terms_of_service)
    if ("id" in response):
        print_success("Repo creat satisfactòriament.")
        print_success(f'🌐 URL: {response.get('html_url')}')
    else:
        print_error("Error al crear el repositori.")