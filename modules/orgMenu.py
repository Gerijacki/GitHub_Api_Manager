from modules.Utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info

class OrgMenu:
    def __init__(self, gestor_orgs):
        self.gestor_orgs = gestor_orgs
        self.opcions_menu = {
            "1": self.llistar_orgs,
            "2": self.veure_detalls_org,
            "3": self.llistar_membres_org,
            "4": self.afegir_membre_org,
            "5": self.eliminar_membre_org,
            "6": self.llistar_repos_org,
            "7": self.crear_repo_org,
            "8": self.sortir
        }

    def gestionar_organitzacions(self):
        while True:
            clear_screen()
            print_info("\n==== GESTIÓ DE LES ORGANITZACIONS ====")
            for clau, accio in self.opcions_menu.items():
                print_info(f"{clau}. {accio.__doc__}")
            
            opcio = input_info("\nSelecciona una opció: ")
            if opcio == "8":
                return  # Retorna al menú anterior

            self.opcions_menu.get(opcio, self.opcio_invàlida)()
            pause()

    def llistar_orgs(self):
        """Llistar les meves organitzacions"""
        orgs = self.gestor_orgs.llistar_orgs()
        print_info("\n=== LES MEVES ORGS ===")
        for org in orgs:
            print_info(f"- {org['login']}")

    def veure_detalls_org(self):
        """Veure detalls d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        detalls = self.gestor_orgs.obtenir_detalls_org(nom_org)

        if not detalls:
            print_error("No s'ha trobat informació.")
            return

        print_info("\n=== Detalls de l'org ===")
        print_info(f"📌 Nom: {detalls.get('name', 'NA')}")
        print_info(f"🔗 URL GITHUB: {detalls.get('html_url', 'NA')}")
        print_info(f"📍 Ubicació: {detalls.get('location', 'NA')}")
        print_info(f"📧 Email: {detalls.get('email', 'NA')}")
        print_info(f"📅 Creada el: {detalls.get('created_at', 'NA')}")
        print_info(f"📅 Última actualització: {detalls.get('updated_at', 'NA')}")
        print_info(f"📝 Descripció: {detalls.get('description', 'NA')}")
        print_info(f"🐦 Twitter: {detalls.get('twitter_username', 'NA')}")
        print_info(f"🖥 Blog: {detalls.get('blog', 'NA')}")
        print_info("\n=== 📊 Estadístiques ===")
        print_info(f"📂 Repos públics: {detalls.get('public_repos', 0)}")
        print_info(f"🔒 Repos privats: {detalls.get('total_private_repos', 0)}")
        print_info(f"⭐ Stars: {detalls.get('followers', 0)}")
        print_info(f"📌 Seguits: {detalls.get('following', 0)}")
        print_info(f"👥 Col·laboradors: {detalls.get('collaborators', 0)}")
        print_info("\n🖼 Avatar:")
        print_info(detalls.get("avatar_url", "NA"))

    def llistar_membres_org(self):
        """Llistar membres d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        membres = self.gestor_orgs.llistar_membres_org(nom_org)
        print_info("\n=== Membres de l'org ===")
        for membre in membres:
            print_info(f"- {membre['login']}")

    def afegir_membre_org(self):
        """Afegir membre a una organització"""
        nom_org = input_info("Nom de l'org: ")
        usuari = input_info("Usuari a afegir: ")
        rol = input_info("Rol (membre/admin): ")
        resposta = self.gestor_orgs.afegir_membre_org(nom_org, usuari, rol)
        print_info(resposta)

    def eliminar_membre_org(self):
        """Eliminar membre d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        usuari = input_info("Usuari a eliminar: ")
        confirmacio = input_warning(f"Estàs segur que vols eliminar l'usuari {usuari} de l'organització {nom_org}? (s/n) ")
        
        if confirmacio.lower() == "s":
            if self.gestor_orgs.eliminar_membre_org(nom_org, usuari):
                print_success("Usuari eliminat correctament.")
            else:
                print_error("Error en eliminar l'usuari.")
        else:
            print_warning("Acció denegada")

    def llistar_repos_org(self):
        """Llistar repositoris d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        repos = self.gestor_orgs.llistar_repos_org(nom_org)
        print_info("\n=== Repos de l'org ===")
        for repo in repos:
            print_info(f"- {repo['name']} ({'Privat' if repo['private'] else 'Públic'})")

    def crear_repo_org(self):
        """Crear un repositori en una organització"""
        nom_org = input_info("Nom de l'org: ")
        nom_repo = input_info("Nom del nou repo: ")
        privat = input_info("Privat? (s/n): ").lower() == "s"
        crear_readme = input_info("Vols incloure un README al repositori? (s/n): ").lower() == "s"
        crear_politica_privacitat = input_info("Vols incloure la política de privacitat? (s/n): ").lower() == "s"
        crear_termes_servei = input_info("Vols incloure la política d'usos? (s/n): ").lower() == "s"

        resposta = self.gestor_orgs.crear_repo_org(nom_org, nom_repo, privat, crear_readme, crear_politica_privacitat, crear_termes_servei)
        if "id" in resposta:
            print_success("Repo creat satisfactòriament.")
            print_success(f'🌐 URL: {resposta.get("html_url")}')
        else:
            print_error("Error al crear el repositori.")

    def sortir(self):
        """Sortir del menú"""
        return

    def opcio_invàlida(self):
        """Opció no vàlida"""
        print_error("Opció no vàlida.")
