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
                self.gestionar_repos()
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
    
    def gestionar_repos(self):
        while True:
            self.clear_screen()
            print("\n==== GESTIÓN DE REPOSITORIOS ====")
            print("1. Listar mis repositorios")
            print("2. Crear un nuevo repositorio")
            print("3. Eliminar un repositorio")
            print("4. Volver al menú principal")

            opcion = input("\nSelecciona una opción: ")

            if opcion == "1":
                self.listar_repos()
            elif opcion == "2":
                self.crear_repo()
            elif opcion == "3":
                self.eliminar_repo()
            elif opcion == "4":
                break
            else:
                print("\nOpción inválida.")

            self.pause()

    def listar_repos(self):
        repos = self.github.list_repos()
        print("\n=== Mis Repositorios ===")
        for repo in repos:
            print(f"- {repo['name']} ({'Privado' if repo['private'] else 'Público'})")

    def crear_repo(self):
        nombre = input("Nombre del nuevo repositorio: ")
        privado = input("¿Privado? (s/n): ").lower() == "s"
        response = self.github.create_repo(nombre, privado)
        if "id" in response:
            print("\n✅ Repositorio creado exitosamente.")
        else:
            print("\n❌ Error al crear el repositorio.")

    def eliminar_repo(self):
        nombre = input("Nombre del repositorio a eliminar: ")
        if self.repo_manager.delete_repo(nombre):
            print("\n✅ Repositorio eliminado.")
        else:
            print("\n❌ Error al eliminar el repositorio.")

    # ================== GESTIÓN DE ORGANIZACIONES ================== #

    def gestionar_organizaciones(self):
        while True:
            self.clear_screen()
            print("\n==== GESTIÓN DE ORGANIZACIONES ====")
            print("1. Listar mis organizaciones")
            print("2. Ver detalles de una organización")
            print("3. Listar miembros de una organización")
            print("4. Añadir miembro a una organización")
            print("5. Eliminar miembro de una organización")
            print("6. Listar repositorios de una organización")
            print("7. Crear un repositorio en una organización")
            print("8. Volver al menú principal")

            opcion = input("\nSelecciona una opción: ")

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
                print("\nOpción inválida.")

            self.pause()

    def listar_orgs(self):
        orgs = self.org_manager.list_orgs()
        print("\n=== Mis Organizaciones ===")
        for org in orgs:
            print(f"- {org['login']}")

    def ver_detalles_org(self):
        org_name = input("Nombre de la organización: ")
        details = self.org_manager.get_org_details(org_name)
        print(details)

    def listar_miembros_org(self):
        org_name = input("Nombre de la organización: ")
        members = self.org_manager.list_org_members(org_name)
        print("\n=== Miembros de la Organización ===")
        for member in members:
            print(f"- {member['login']}")

    def agregar_miembro_org(self):
        org_name = input("Nombre de la organización: ")
        username = input("Usuario a agregar: ")
        role = input("Rol (member/admin): ")
        response = self.org_manager.add_member_to_org(org_name, username, role)
        print(response)

    def eliminar_miembro_org(self):
        org_name = input("Nombre de la organización: ")
        username = input("Usuario a eliminar: ")
        if self.org_manager.remove_member_from_org(org_name, username):
            print("✅ Usuario eliminado correctamente.")
        else:
            print("❌ Error al eliminar usuario.")

    def listar_repos_org(self):
        org_name = input("Nombre de la organización: ")
        repos = self.org_manager.list_org_repos(org_name)
        print("\n=== Repositorios de la Organización ===")
        for repo in repos:
            print(f"- {repo['name']} ({'Privado' if repo['private'] else 'Público'})")

    def crear_repo_org(self):
        org_name = input("Nombre de la organización: ")
        repo_name = input("Nombre del nuevo repositorio: ")
        privado = input("¿Privado? (s/n): ").lower() == "s"
        response = self.org_manager.create_org_repo(org_name, repo_name, privado)
        print(response)

    # ================== ESTADÍSTICAS ================== #

    def ver_stats_repo(self):
        owner = input("Usuario/Organización dueña del repo: ")
        repo = input("Nombre del repositorio: ")
        stats = self.stats_manager.get_repo_stats(owner, repo)
        print("\n=== Estadísticas de Contribuyentes ===")
        if isinstance(stats, list):
            for contributor in stats:
                print(f"- {contributor['author']['login']}: {contributor['total']} contribuciones")
        else:
            print("\n❌ No hay datos disponibles aún.")

