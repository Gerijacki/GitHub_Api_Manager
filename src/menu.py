from src.Github import GitHub
from src.modules.Utils import *

class Menu:
    def __init__(self):
        self.github = GitHub()

    def mostrar_menu(self):
        clear_screen()
        self.ver_usuario()
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
