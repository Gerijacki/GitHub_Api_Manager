import os
import sys
from github import GitHub
from modules.repo import RepoManager
from modules.org import OrgManager
from modules.stats import StatsManager

class Menu:
    def __init__(self):
        self.github = GitHub()
        self.repo_manager = RepoManager()
        self.org_manager = OrgManager()
        self.stats_manager = StatsManager()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("\Prem Enter per continuar...")

    def mostrar_menu(self):
        while True:
            self.clear_screen()
            print("\n==== GESTOR DE GITHUB ====")
            print("1. Veure informació de l'usuari")
            print("2. Gestionar Repos")
            print("3. Gestionar Organitzacions")
            print("4. Veure estadístiques d'un repositori")
            print("5. Salir")

            opcion = input("\nSel·lecciona una opció: ")

            if opcion == "1":
                self.ver_usuario()
            elif opcion == "2":
                self.gestionar_repo()
            elif opcion == "3":
                self.gestionar_organizaciones()
            elif opcion == "4":
                self.ver_stats_repo()
            elif opcion == "5":
                print("\Sortint...")
                sys.exit()
            else:
                print("\nOpció invàlida.")

            self.pause()

    def ver_usuario(self):
        user = self.github.get_user()
        print("\n=== Informació de l'usuari ===")
        print(f"👤 Nom d'usuari: {user.get('login')}")
        print(f"📛 Nom complet: {user.get('name', 'No disponible')}")
        print(f"📍 Ubicació: {user.get('location', 'No disponible')}")
        print(f"📧 Correu electrònic: {user.get('email', 'No disponible')}")
        print(f"🏢 Empresa: {user.get('company', 'No disponible')}")
        print(f"🌐 Blog: {user.get('blog', 'No disponible')}")
        print(f"🐦 Twitter: @{user.get('twitter_username', 'No disponible')}")
        print(f"📖 Biografia: {user.get('bio', 'No disponible')}")
        print(f"📅 Data de creació: {user.get('created_at')}")
        print(f"🔄 Última actualització: {user.get('updated_at')}")
        print(f"📂 Repositoris públics: {user.get('public_repos')}")
        print(f"🔒 Repositoris privats: {user.get('total_private_repos')}")
        print(f"⭐ Seguidors: {user.get('followers')}")
        print(f"👥 Seguint: {user.get('following')}")
        print(f"📦 Espai d'emmagatzematge usat: {user.get('disk_usage')} KB")
        print(f"🔗 Perfil de GitHub: {user.get('html_url')}")
        print(f"🖼 Avatar: {user.get('avatar_url')}")

    # ================== GESTIÓ DE REPOS ================== #
    
    def gestionar_repo(self):

        while True:
            self.clear_screen()
            print(f"\n=== Gestio dels repositoris ===")
            print("1. Crear un repositori")
            print("2. Eliminar un repositori")
            print("3. Crear una nova branca")
            print("4. Eliminar una branca")
            print("5. Fusionar dues branca")
            print("6. Crear una pull request")
            print("7. Llistar pull requests")
            print("8. Fer merge d'una pull request")
            print("9. Tancar una pull request sense merge")
            print("10. Afegir un col·laborador")
            print("11. Llistar col·laboradors")
            print("12. Tornar al menú principal")

            opcion = input("\nSel·lecciona una opció: ")

            if opcion == "1":
                nombre = input("Nom del nou repo: ")
                privado = input("Privat? (s/n): ").lower() == "s"
                descripcion = input("Descripció del repo: ")

                crear_readme = input("Vols afegir un fitxer README.md? (s/n): ").lower() == "s"
                crear_licencia = input("Vols afegir una llicència? (s/n): ").lower() == "s"
                
                response = self.repo_manager.create_repo(nombre, privado, descripcion, crear_readme, crear_licencia)
                
                print("✅ Repo creat satisfactòriament.") if "id" in response else print("❌ Error al crear el repositori.")

            elif opcion == "2":
                repo_name = input("Nom del repo a eliminar: ")
                confirm = input("Estàs segur que vols eliminar el repo? (s/n)")
                if (confirm.lower() == "s"):
                    if self.repo_manager.delete_repo(repo_name):
                        print("✅ Repo eliminat.")
                    else:
                        print("❌ Error en eliminar el repo.")
                else:
                    print('Acció abortada!')

            elif opcion == "3":
                repo_name = input("Nom del repo: ")
                new_branch = input("Nom de la nova branca: ")
                base_branch = input("Branca base (per defecte 'main'): ") or "main"
                response = self.repo_manager.create_branch(repo_name, new_branch, base_branch)
                if(response.get('url')):
                   print(f'✅ Branca generada correctament')
                else:
                    print('❌ Error al generar la branca')

            elif opcion == "4":
                repo_name = input("Nom del repo: ")
                branch_name = input("Nom de la branca a eliminar: ")
                if self.repo_manager.delete_branch(repo_name, branch_name):
                    print("✅ Branca eliminada correctament.")
                else:
                    print("❌ Error en eliminar la branca.")

            elif opcion == "5":
                repo_name = input("Nom del repo: ")
                base = input("Branca base (destí del merge): ")
                head = input("Branca a fusionar (origen del merge): ")
                response = self.repo_manager.merge_branches(repo_name, base, head)
                print(response)

            elif opcion == "6":
                repo_name = input("Nom del repo: ")
                title = input("Títol de la PR: ")
                head = input("Branca d'origen: ")
                base = input("Branca de destí (per defecte 'main'): ") or "main"
                body = input("Descripció de la PR: ")
                response = self.repo_manager.create_pull_request(repo_name, title, head, base, body)
                if (response.get('number')):
                    print("✅ PR generada correctament.")
                    print("\n=== Detalls de la PR ===")
                    print(f'🆔 ID: {response.get('number')} ')
                    print(f'⛓️‍💥 URL: {response.get('html_url')} ')
                    print(f'👁️ BODY: {response.get('body')} ')
                else:
                    print

            elif opcion == "7":
                repo_name = input("Nom del repo: ")
                prs = self.repo_manager.list_pull_requests(repo_name)
                print("\n=== Pull Requests Obertes ===")
                for pr in prs:
                    print(f"- #{pr['number']} {pr['title']} ({pr['state']})")

            elif opcion == "8":
                repo_name = input("Nom del repo: ")
                pr_number = input("Número de la PR a fusionar: ")
                response = self.repo_manager.merge_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "9":
                repo_name = input("Nom del repo: ")
                pr_number = input("Número de la PR a tancar: ")
                response = self.repo_manager.close_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "10":
                repo_name = input("Nom del repo: ")
                collaborator = input("Usuari a afegir: ")
                permission = input("Permisos (pull/push/admin): ")
                if self.repo_manager.add_collaborator(repo_name, collaborator, permission):
                    print("✅ Col·laborador afegit correctament")
                else:
                    print("❌ Error en afegir el col·laborador.")

            elif opcion == "11":
                repo_name = input("Nom del repo: ")
                collaborators = self.repo_manager.list_collaborators(repo_name)
                print("\n=== Col·laboradors del repo ===")
                for collaborator in collaborators:
                    print(f"- {collaborator['login']} ({collaborator['permissions']})")

            elif opcion == "12":
                break

            else:
                print("\nOpció no vàlida.")

            self.pause()

# ================== GESTIÓ D'ESTADÍSTIQUES DEL REPO ================== #
    
    def ver_stats_repo(self):
        owner = input("Propietari del repo: ")
        repo_name = input("Nom del repo: ")

        while True:
            self.clear_screen()
            print(f"\n=== Estadístiques del repo: {repo_name} ===")
            print("1. Veure resum general")
            print("2. Veure commits recents")
            print("3. Veure branques del repo")
            print("4. Veure releases del repo")
            print("5. Veure issues obertes")
            print("6. Veure pull requests obertes")
            print("7. Tornar al menú principal")

            opcion = input("\nSel·lecciona una opció: ")

            if opcion == "1":
                stats = self.stats_manager.get_repo_overview(owner, repo_name)
                print("\n=== Resum del repo ===")
                for key, value in stats.items():
                    print(f"{key}: {value}")

            elif opcion == "2":
                commits = self.stats_manager.get_repo_commits(owner, repo_name)
                print("\n=== Últims commits ===")
                for commit in commits[:5]:  # Mostramos los últimos 5 commits
                    print(f"- {commit['commit']['message']} ({commit['commit']['author']['name']})")

            elif opcion == "3":
                branches = self.stats_manager.get_repo_branches(owner, repo_name)
                print("\n=== Branques del repo ===")
                for branch in branches:
                    print(f"- {branch['name']}")

            elif opcion == "4":
                releases = self.stats_manager.get_repo_releases(owner, repo_name)
                print("\n=== Releases del repo ===")
                for release in releases:
                    print(f"- {release['name']} (Tag: {release['tag_name']})")

            elif opcion == "5":
                issues = self.stats_manager.get_repo_issues(owner, repo_name)
                print("\n=== Issues Obertes ===")
                for issue in issues:
                    print(f"- #{issue['number']} {issue['title']} (Estado: {issue['state']})")

            elif opcion == "6":
                prs = self.stats_manager.get_repo_pull_requests(owner, repo_name)
                print("\n=== Pull Requests Obertes ===")
                for pr in prs:
                    print(f"- #{pr['number']} {pr['title']} ({pr['state']})")

            elif opcion == "7":
                break

            else:
                print("\nOpció no vàlida.")

            self.pause()

            # ================== GESTIÓN DE ORGANIZACIONES ================== #

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
        print(f"📦 Membres poden crear repos: {'Sí' if details.get('members_can_create_repositories', False) else 'No'}")
        print(f"📢 Membres poden crear repos públics: {'Sí' if details.get('members_can_create_public_repositories', False) else 'No'}")
        print(f"🔒 Membres poden crear repos privats: {'Sí' if details.get('members_can_create_private_repositories', False) else 'No'}")
        
        print("\n🖼 Avatar:")
        print(details.get('avatar_url', 'NA'))

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