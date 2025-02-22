from src.modules.Utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info

class OrgMenu:
    def __init__(self, OrgManager):
        self.OrgManager = OrgManager
        self.opcions_menu = {
            "1": self.llistar_orgs,
            "2": self.veure_detalls_org,
            "3": self.llistar_repos_org,
            "4": self.llistar_membres_org,
            "5": self.afegir_membre_org,
            "6": self.eliminar_membre_org,
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
        try:
            orgs = self.OrgManager.list_orgs()
            if not orgs:
                print_warning("No s'han trobat organitzacions.")
                return
            print_info("\n=== LES MEVES ORGS ===")
            for org in orgs:
                print_info(f"- {org['login']}")
        except Exception as e:
            print_error(f"Error al llistar organitzacions: {str(e)}")

    def veure_detalls_org(self):
        """Veure detalls d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        try:
            detalls = self.OrgManager.get_org_details(nom_org)

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
        except Exception as e:
            print_error(f"Error al veure els detalls de l'organització: {str(e)}")

    def llistar_membres_org(self):
        """Llistar membres d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        try:
            membres = self.OrgManager.list_org_members(nom_org)
            if not membres:
                print_warning(f"No s'han trobat membres per l'organització {nom_org}.")
                return
            print_info("\n=== Membres de l'org ===")
            for membre in membres:
                print_info(f"- {membre['login']}")
        except Exception as e:
            print_error(f"Error al llistar membres de l'organització: {str(e)}")

    def afegir_membre_org(self):
        """Afegir un membre a una organització de GitHub"""
        
        nom_org = input_info("Nom de l'organització: ")
        usuari = input_info("Nom d'usuari a afegir: ")
        rol = input_info("Rol ('member' o 'admin'): ").lower()

        if rol not in ["member", "admin"]:
            print_error("Rol invàlid! Ha de ser 'member' o 'admin'.")
            return
        try:
            resposta = self.OrgManager.add_member_to_org(nom_org, usuari, rol)
            
            if resposta.get("status") == "success":
                print_info(f"✅ L'usuari {usuari} s'ha afegit correctament a {nom_org} amb el rol '{rol}'.")
            else:
                print_warning(f"⚠️ No s'ha pogut afegir {usuari}. Resposta: {resposta}")
        except Exception as e:
            print_error(f"❌ Error en afegir membre: {str(e)}")

    def eliminar_membre_org(self):
        """Eliminar membre d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        usuari = input_info("Usuari a eliminar: ")
        confirmacio = input_warning(f"Estàs segur que vols eliminar l'usuari {usuari} de l'organització {nom_org}? (s/n) ")
        
        if confirmacio.lower() == "s":
            try:
                if self.OrgManager.remove_member_from_org(nom_org, usuari):
                    print_success("Usuari eliminat correctament.")
                else:
                    print_error("Error en eliminar l'usuari.")
            except Exception as e:
                print_error(f"Error en eliminar l'usuari: {str(e)}")
        else:
            print_warning("Acció denegada")

    def llistar_repos_org(self):
        """Llistar repositoris d'una organització"""
        nom_org = input_info("Nom de l'org: ")
        try:
            repos = self.OrgManager.list_org_repos(nom_org)
            if not repos:
                print_warning(f"No s'han trobat repositoris per l'organització {nom_org}.")
                return
            print_info("\n=== Repos de l'org ===")
            for repo in repos:
                print_info(f"- {repo['name']} ({'Privat' if repo['private'] else 'Públic'})")
        except Exception as e:
            print_error(f"Error al llistar repositoris de l'organització: {str(e)}")

    def crear_repo_org(self):
        """Crear un repositori en una organització"""
        nom_org = input_info("Nom de l'org: ")
        nom_repo = input_info("Nom del nou repo: ")

        if not nom_repo.strip():
            print_error("El nom del repositori no pot estar buit.")
            return
        
        privat = input_info("Privat? (s/n): ").lower() == "s"
        crear_readme = input_info("Vols incloure un README al repositori? (s/n): ").lower() == "s"
        crear_politica_privacitat = input_info("Vols incloure la política de privacitat? (s/n): ").lower() == "s"
        crear_termes_servei = input_info("Vols incloure la política d'usos? (s/n): ").lower() == "s"

        try:
            resposta = self.OrgManager.create_org_repo(nom_org, nom_repo, privat, crear_readme, crear_politica_privacitat, crear_termes_servei)
            if "id" in resposta:
                print_success("Repo creat satisfactòriament.")
                print_success(f'🌐 URL: {resposta.get("html_url")}')
            else:
                print_error("Error al crear el repositori.")
        except Exception as e:
            print_error(f"Error en crear el repositori: {str(e)}")

    def sortir(self):
        """Sortir del menú"""
        return

    def opcio_invàlida(self):
        """Opció no vàlida"""
        print_error("Opció no vàlida.")
