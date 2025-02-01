import os
# ================== GESTIÓ DE REPOS ================== #
class RepoMenu:
    def __init__(self, repo_manager):
        self.repo_manager = repo_manager

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("Prem Enter per continuar...")

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

                crear_readme = (
                    input("Vols afegir un fitxer README.md? (s/n): ").lower() == "s"
                )
                crear_licencia = (
                    input("Vols afegir una llicència? (s/n): ").lower() == "s"
                )

                response = self.repo_manager.create_repo(
                    nombre, privado, descripcion, crear_readme, crear_licencia
                )

                (
                    print("✅ Repo creat satisfactòriament.")
                    if "id" in response
                    else print("❌ Error al crear el repositori.")
                )

            elif opcion == "2":
                repo_name = input("Nom del repo a eliminar: ")
                confirm = input("Estàs segur que vols eliminar el repo? (s/n)")
                if confirm.lower() == "s":
                    if self.repo_manager.delete_repo(repo_name):
                        print("✅ Repo eliminat.")
                    else:
                        print("❌ Error en eliminar el repo.")
                else:
                    print("Acció abortada!")

            elif opcion == "3":
                repo_name = input("Nom del repo: ")
                new_branch = input("Nom de la nova branca: ")
                base_branch = input("Branca base (per defecte 'main'): ") or "main"
                response = self.repo_manager.create_branch(
                    repo_name, new_branch, base_branch
                )
                if response.get("url"):
                    print(f"✅ Branca generada correctament")
                else:
                    print("❌ Error al generar la branca")

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
                response = self.repo_manager.create_pull_request(
                    repo_name, title, head, base, body
                )
                if response.get("number"):
                    print("✅ PR generada correctament.")
                    print("\n=== Detalls de la PR ===")
                    print(f"🆔 ID: {response.get('number')} ")
                    print(f"⛓️‍💥 URL: {response.get('html_url')} ")
                    print(f"👁️ BODY: {response.get('body')} ")
                else:
                    print("❌ Error en crear la PR.")

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
                if self.repo_manager.add_collaborator(
                    repo_name, collaborator, permission
                ):
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