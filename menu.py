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
        input("\nPresiona Enter para continuar...")

    def mostrar_menu(self):
        while True:
            self.clear_screen()
            print("\n==== GESTOR DE GITHUB ====")
            print("1. Ver información del usuario")
            print("2. Gestionar Repositorios")
            print("3. Gestionar Organizaciones")
            print("4. Ver estadísticas de un repositorio")
            print("5. Salir")

            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":
                self.ver_usuario()
            elif opcion == "2":
                self.gestionar_repo()
            elif opcion == "3":
                self.gestionar_organizaciones()
            elif opcion == "4":
                self.ver_stats_repo()
            elif opcion == "5":
                print("\nSaliendo...")
                sys.exit()
            else:
                print("\nOpción inválida.")

            self.pause()

    def ver_usuario(self):
        user = self.github.get_user()
        print("\n=== Información del Usuario ===")
        print(f"Nombre: {user.get('name', 'Desconocido')}")
        print(f"Usuario: {user.get('login')}")
        print(f"Email: {user.get('email', 'No disponible')}")
        print(f"Repositorios públicos: {user.get('public_repos')}")

    # ================== GESTIÓN DE REPOSITORIOS ================== #
    
    def gestionar_repo(self):

        while True:
            self.clear_screen()
            print(f"\n=== Gestión del Repositorio {repo_name} ===")
            print("1. Crear un repositorio")
            print("2. Eliminar un repositorio")
            print("3. Crear una nueva rama")
            print("4. Eliminar una rama")
            print("5. Fusionar dos ramas")
            print("6. Crear un pull request")
            print("7. Listar pull requests")
            print("8. Hacer merge a un pull request")
            print("9. Cerrar un pull request sin merge")
            print("10. Agregar un colaborador")
            print("11. Listar colaboradores")
            print("12. Volver al menú principal")

            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":
                nombre = input("Nombre del nuevo repositorio: ")
                privado = input("¿Privado? (s/n): ").lower() == "s"
                descripcion = input("Descripción del repositorio: ")
                response = self.repo_manager.create_repo(nombre, privado, descripcion)
                print("\n✅ Repositorio creado exitosamente.") if "id" in response else print("\n❌ Error al crear el repositorio.")

            elif opcion == "2":
                repo_name = input("Nombre del repositorio a eliminar: ")
                confirm = input("Estas seguro que quieres eliminar el repositorio? (s/n)")
                if (confirm.lower() == "s"):
                    if self.repo_manager.delete_repo(repo_name):
                        print("\n✅ Repositorio eliminado.")
                    else:
                        print("\n❌ Error al eliminar el repositorio.")
                else:
                    print('Acció cancelada!')

            elif opcion == "3":
                repo_name = input("Nombre del repositorio: ")
                new_branch = input("Nombre de la nueva rama: ")
                base_branch = input("Rama base (por defecto 'main'): ") or "main"
                response = self.repo_manager.create_branch(repo_name, new_branch, base_branch)
                print(response)

            elif opcion == "4":
                repo_name = input("Nombre del repositorio: ")
                branch_name = input("Nombre de la rama a eliminar: ")
                if self.repo_manager.delete_branch(repo_name, branch_name):
                    print("\n✅ Rama eliminada correctamente.")
                else:
                    print("\n❌ Error al eliminar la rama.")

            elif opcion == "5":
                repo_name = input("Nombre del repositorio: ")
                base = input("Rama base (destino del merge): ")
                head = input("Rama a fusionar (origen del merge): ")
                response = self.repo_manager.merge_branches(repo_name, base, head)
                print(response)

            elif opcion == "6":
                repo_name = input("Nombre del repositorio: ")
                title = input("Título del PR: ")
                head = input("Rama de origen: ")
                base = input("Rama de destino (por defecto 'main'): ") or "main"
                body = input("Descripción del PR: ")
                response = self.repo_manager.create_pull_request(repo_name, title, head, base, body)
                print(response)

            elif opcion == "7":
                repo_name = input("Nombre del repositorio: ")
                prs = self.repo_manager.list_pull_requests(repo_name)
                print("\n=== Pull Requests Abiertos ===")
                for pr in prs:
                    print(f"- #{pr['number']} {pr['title']} ({pr['state']})")

            elif opcion == "8":
                repo_name = input("Nombre del repositorio: ")
                pr_number = input("Número del PR a fusionar: ")
                response = self.repo_manager.merge_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "9":
                repo_name = input("Nombre del repositorio: ")
                pr_number = input("Número del PR a cerrar: ")
                response = self.repo_manager.close_pull_request(repo_name, pr_number)
                print(response)

            elif opcion == "10":
                repo_name = input("Nombre del repositorio: ")
                collaborator = input("Usuario a agregar: ")
                permission = input("Permiso (pull/push/admin): ")
                if self.repo_manager.add_collaborator(repo_name, collaborator, permission):
                    print("\n✅ Colaborador agregado correctamente.")
                else:
                    print("\n❌ Error al agregar colaborador.")

            elif opcion == "11":
                repo_name = input("Nombre del repositorio: ")
                collaborators = self.repo_manager.list_collaborators(repo_name)
                print("\n=== Colaboradores del Repositorio ===")
                for collaborator in collaborators:
                    print(f"- {collaborator['login']} ({collaborator['permissions']})")

            elif opcion == "12":
                break

            else:
                print("\nOpción inválida.")

            self.pause()
