import sys
from src.Github import GitHub
from src.modules.RepoManager import RepoManager
from src.modules.OrgManager import OrgManager
from src.modules.StatsManager import StatsManager
from src.modules.OrgMenu import OrgMenu
from src.modules.RepoMenu import RepoMenu
from src.modules.StatsMenu import StatsMenu
from src.modules.Utils import clear_screen, pause, print_error, print_info, print_success, print_warning

class Menu:
    def __init__(self):
        self.github = GitHub()
        self.repo_manager = RepoManager()
        self.org_manager = OrgManager()
        self.stats_manager = StatsManager()
        self.org_menu = OrgMenu(self.org_manager)
        self.stats_menu = StatsMenu(self.stats_manager)
        self.repo_menu = RepoMenu(self.repo_manager)

    def mostrar_menu(self):
        while True:
            clear_screen()
            print("\n==== GESTOR DE GITHUB ====")
            print_info("1. Veure informació de l'usuari [ 🚻 ]")
            print_info("2. Gestionar Repos [ 💭 ]")
            print_info("3. Gestionar Organitzacions [ 🗄️ ]")
            print_info("4. Veure estadístiques d'un repositori [ 💱 ]")
            print_info("5. Salir [ 🏳️ ]")

            opcion = input("\nSel·lecciona una opció: ")

            if opcion == "1":
                self.ver_usuario()
            elif opcion == "2":
                self.repo_menu.gestionar_repo()
            elif opcion == "3":
                self.org_menu.gestionar_organitzacions()
            elif opcion == "4":
                self.stats_menu.ver_stats_repo()
            elif opcion == "5":
                print_warning("Sortint...")
                sys.exit()
            else:
                print_error("\nOpció invàlida.")

            pause()

    def ver_usuario(self):
        user = self.github.get_user()
        print_info("\n=== Informació de l'usuari ===")
        print_info(f"👤 Nom d'usuari: {user.get('login')}")
        print_info(f"📛 Nom complet: {user.get('name', 'No disponible')}")
        print_info(f"📍 Ubicació: {user.get('location', 'No disponible')}")
        print_info(f"📧 Correu electrònic: {user.get('email', 'No disponible')}")
        print_info(f"🏢 Empresa: {user.get('company', 'No disponible')}")
        print_info(f"🌐 Blog: {user.get('blog', 'No disponible')}")
        print_info(f"🐦 Twitter: @{user.get('twitter_username', 'No disponible')}")
        print_info(f"📖 Biografia: {user.get('bio', 'No disponible')}")
        print_info(f"📅 Data de creació: {user.get('created_at')}")
        print_info(f"🔄 Última actualització: {user.get('updated_at')}")
        print_info(f"📂 Repositoris públics: {user.get('public_repos')}")
        print_info(f"🔒 Repositoris privats: {user.get('total_private_repos')}")
        print_info(f"⭐ Seguidors: {user.get('followers')}")
        print_info(f"👥 Seguint: {user.get('following')}")
        print_info(f"📦 Espai d'emmagatzematge usat: {user.get('disk_usage')} KB")
        print_info(f"🔗 Perfil de GitHub: {user.get('html_url')}")
        print_info(f"🖼 Avatar: {user.get('avatar_url')}")
