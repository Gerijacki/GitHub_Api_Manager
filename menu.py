import os
import sys
from github import GitHub
from modules.repoManager import RepoManager
from modules.orgManager import OrgManager
from modules.statsManager import StatsManager
from modules.orgMenu import OrgMenu
from modules.repoMenu import RepoMenu
from modules.statsMenu import StatsMenu

class Menu:
    def __init__(self):
        self.github = GitHub()
        self.repo_manager = RepoManager()
        self.org_manager = OrgManager()
        self.stats_manager = StatsManager()
        self.org_menu = OrgMenu(self.org_manager)
        self.stats_menu = StatsMenu(self.stats_manager)
        self.repo_menu = RepoMenu(self.repo_manager)

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("Prem Enter per continuar...")

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
                self.repo_menu.gestionar_repo()
            elif opcion == "3":
                self.org_menu.gestionar_organizaciones()
            elif opcion == "4":
                self.stats_menu.ver_stats_repo()
            elif opcion == "5":
                print("Sortint...")
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
