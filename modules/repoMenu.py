from modules.utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info
# ================== GESTIÓ DE REPOS ================== #
class RepoMenu:
    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def gestionar_repo(self):

        while True:
            clear_screen()
            print_info(f"\n=== Gestio dels repositoris ===")
            print_info("1. Crear un repositori")
            print_info("2. Eliminar un repositori")
            print_info("3. Crear una nova branca")
            print_info("4. Eliminar una branca")
            print_info("5. Fusionar dues branca")
            print_info("6. Crear una pull request")
            print_info("7. Llistar pull requests")
            print_info("8. Fer merge d'una pull request")
            print_info("9. Tancar una pull request sense merge")
            print_info("10. Afegir un col·laborador")
            print_info("11. Llistar col·laboradors")
            print_info("12. Tornar al menú principal")

            opcion = input_info("\nSel·lecciona una opció: ")

            if opcion == "1":
                nombre = input_info("Nom del nou repo: ")
                privado = input_info("Privat? (s/n): ").lower() == "s"
                descripcion = input_info("Descripció del repo: ")

                crear_readme = (
                    input_info("Vols afegir un fitxer README.md? (s/n): ").lower() == "s"
                )
                crear_licencia = (
                    input_info("Vols afegir una llicència? (s/n): ").lower() == "s"
                )

                response = self.repo_manager.create_repo(
                    nombre, privado, descripcion, crear_readme, crear_licencia
                )

                (
                    print_success("Repo creat satisfactòriament.")
                    if "id" in response
                    else print_error("Error al crear el repositori.")
                )

            elif opcion == "2":
                repo_name = input_info("Nom del repo a eliminar: ")
                confirm = input_warning("Estàs segur que vols eliminar el repo? (s/n)")
                if confirm.lower() == "s":
                    if self.repo_manager.delete_repo(repo_name):
                        print_success("Repo eliminat.")
                    else:
                        print_error("Error en eliminar el repo.")
                else:
                    print_warning("Acció abortada!")

            elif opcion == "3":
                repo_name = input_info("Nom del repo: ")
                new_branch = input_info("Nom de la nova branca: ")
                base_branch = input_info("Branca base (per defecte 'main'): ") or "main"
                response = self.repo_manager.create_branch(
                    repo_name, new_branch, base_branch
                )
                if response.get("url"):
                    print_success(f"Branca generada correctament")
                else:
                    print_error("Error al generar la branca")

            elif opcion == "4":
                repo_name = input_info("Nom del repo: ")
                branch_name = input_warning("Nom de la branca a eliminar: ")
                if self.repo_manager.delete_branch(repo_name, branch_name):
                    print_success("Branca eliminada correctament.")
                else:
                    print_error("Error en eliminar la branca.")

            elif opcion == "5":
                repo_name = input_info("Nom del repo: ")
                base = input_info("Branca base (destí del merge): ")
                head = input_info("Branca a fusionar (origen del merge): ")
                response = self.repo_manager.merge_branches(repo_name, base, head)
                print(response)

            elif opcion == "6":
                repo_name = input_info("Nom del repo: ")
                title = input_info("Títol de la PR: ")
                head = input_info("Branca d'origen: ")
                base = input_info("Branca de destí (per defecte 'main'): ") or "main"
                body = input_info("Descripció de la PR: ")
                response = self.repo_manager.create_pull_request(
                    repo_name, title, head, base, body
                )
                if response.get("number"):
                    print_success("PR generada correctament.")
                    print_info("\n=== Detalls de la PR ===")
                    print_info(f"🆔 ID: {response.get('number')} ")
                    print_info(f"⛓️‍💥 URL: {response.get('html_url')} ")
                    print_info(f"👁️ BODY: {response.get('body')} ")
                else:
                    print_error("Error en crear la PR.")

            elif opcion == "7":
                repo_name = input("Nom del repo: ")
                prs = self.repo_manager.list_pull_requests(repo_name)
                print_info("\n=== Pull Requests Obertes ===")
                for pr in prs:
                    print_info(f"- #{pr['number']} {pr['title']} ({pr['state']})")

            elif opcion == "8":
                repo_name = input_info("Nom del repo: ")
                pr_number = input_info("Número de la PR a fusionar: ")
                response = self.repo_manager.merge_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "9":
                repo_name = input_info("Nom del repo: ")
                pr_number = input_warning("Número de la PR a tancar: ")
                response = self.repo_manager.close_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "10":
                repo_name = input_info("Nom del repo: ")
                collaborator = input_info("Usuari a afegir: ")
                permission = input_info("Permisos (pull/push/admin): ")
                if self.repo_manager.add_collaborator(
                    repo_name, collaborator, permission
                ):
                    print_success("Col·laborador afegit correctament")
                else:
                    print_error("Error en afegir el col·laborador.")

            elif opcion == "11":
                repo_name = input_info("Nom del repo: ")
                collaborators = self.repo_manager.list_collaborators(repo_name)
                print_info("\n=== Col·laboradors del repo ===")
                for collaborator in collaborators:
                    print_info(f"- {collaborator['login']} ({collaborator['permissions']})")

            elif opcion == "12":
                break

            else:
                print_error("\nOpció no vàlida.")

            pause()