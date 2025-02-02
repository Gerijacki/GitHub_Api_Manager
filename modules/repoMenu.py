from modules.Utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info

class RepoMenu:
    def __init__(self, gestor_repos):
        self.gestor_repos = gestor_repos
        self.opcions_menu = {
            "1": self.crear_repositori,
            "2": self.eliminar_repositori,
            "3": self.llistar_branques,
            "4": self.crear_branques,
            "5": self.eliminar_branques,
            "6": self.fusionar_branques,
            "7": self.crear_pull_request,
            "8": self.llistar_pull_requests,
            "9": self.fer_merge_pull_request,
            "10": self.tancar_pull_request,
            "11": self.afegir_colaborador,
            "12": self.llistar_colaboradors,
            "13": self.sortir
        }

    def gestionar_repo(self):
        while True:
            clear_screen()
            print_info("\n=== Gestió dels repositoris ===")
            for key, action in self.opcions_menu.items():
                print_info(f"{key}. {action.__doc__}")
            
            opcio = input_info("\nSelecciona una opció: ")
            if opcio == "13":
                return
            
            self.opcions_menu.get(opcio, self.opcio_invalida)()

            pause()

    def crear_repositori(self):
        """Crear un repositori"""
        nom = input_info("Nom del nou repo: ")
        privat = input_info("Privat? (s/n): ").lower() == "s"
        descripcio = input_info("Descripció del repo: ")
        afegir_readme = input_info("Afegir README.md? (s/n): ").lower() == "s"
        afegir_licencia = input_info("Afegir llicència? (s/n): ").lower() == "s"

        resposta = self.gestor_repos.create_repo(nom, privat, descripcio, afegir_readme, afegir_licencia)
        if "id" in resposta:
            print_success("Repo creat satisfactòriament.")
            print_success(f'🌐 URL: {resposta.get("html_url")}')
        else:
            print_error("Error al crear el repositori.")

    def eliminar_repositori(self):
        """Eliminar un repositori"""
        nom_repo = input_info("Nom del repo a eliminar: ")
        confirmacio = input_warning("Estàs segur? (s/n): ")
        if confirmacio.lower() == "s":
            if self.gestor_repos.delete_repo(nom_repo):
                print_success("Repo eliminat.")
            else:
                print_error("Error en eliminar el repo.")
        else:
            print_warning("Acció cancel·lada!")

    def llistar_branques(self):
        """Llistar branques d'un repositori"""
        nom_repo = input_info("Nom del repo: ")
        branques = self.gestor_repos.list_branches(nom_repo)
        if branques:
            print_info("\n=== Branques del repositori ===")
            for branca in branques:
                print_info(f"- {branca['name']}")
        else:
            print_error("No s'han trobat branques o hi ha un error.")

    def crear_branques(self):
        """Crear una nova branca"""
        nom_repo = input_info("Nom del repo: ")
        nova_branque = input_info("Nom de la nova branca: ")
        branca_base = input_info("Branca base (per defecte 'main'): ") or "main"

        resposta = self.gestor_repos.create_branch(nom_repo, nova_branque, branca_base)
        if resposta.get("url"):
            print_success("Branca creada correctament.")
        else:
            print_error("Error en crear la branca.")

    def eliminar_branques(self):
        """Eliminar una branca"""
        nom_repo = input_info("Nom del repo: ")
        nom_branque = input_warning("Nom de la branca a eliminar: ")
        confirmacio = input_warning(f"Eliminar la branca {nom_branque}? (s/n): ")
        if confirmacio.lower() == "s":
            if self.gestor_repos.delete_branch(nom_repo, nom_branque):
                print_success("Branca eliminada correctament.")
            else:
                print_error("Error en eliminar la branca.")
        else:
            print_warning("Acció cancel·lada!")

    def fusionar_branques(self):
        """Fusionar dues branques"""
        nom_repo = input_info("Nom del repo: ")
        head = input_info("Branca origen: ")
        base = input_info("Branca destí: ")
        resposta = self.gestor_repos.merge_branches(nom_repo, base, head)

        if resposta.get("message"):
            print_success(f"Merge completat de {head} cap a {base}")
            print_success(f'🌐 URL: {resposta.get("html_url")}')
            print_success(f'🚀 Commit message: {resposta.get("message")}')
        else:
            print_error("Error en el merge. Verifica l'estat a GitHub.")

    def crear_pull_request(self):
        """Crear una pull request"""
        nom_repo = input_info("Nom del repo: ")
        titol = input_info("Títol de la PR: ")
        head = input_info("Branca d'origen: ")
        base = input_info("Branca de destí (per defecte 'main'): ") or "main"
        cos = input_info("Descripció de la PR: ")

        resposta = self.gestor_repos.create_pull_request(nom_repo, titol, head, base, cos)
        if resposta.get("number"):
            print_success("PR creada correctament.")
            print_info(f" 🆔 ID: {resposta.get('number')} ")
            print_info(f" ⛓️‍💥 URL: {resposta.get('html_url')} ")
        else:
            print_error("Error en crear la PR.")

    def llistar_pull_requests(self):
        """Llistar pull requests obertes"""
        nom_repo = input_info("Nom del repo: ")
        prs = self.gestor_repos.list_pull_requests(nom_repo)
        print_info("\n=== Pull Requests Obertes ===")
        for pr in prs:
            print_info(f"- #{pr['number']} {pr['title']} ({pr['state']})")

    def fer_merge_pull_request(self):
        """Fer merge d'una pull request"""
        nom_repo = input_info("Nom del repo: ")
        pr_number = input_info("Número de la PR a fusionar: ")
        resposta = self.gestor_repos.merge_pull_request(nom_repo, pr_number)

        if resposta.get("merged"):
            print_success("Pull request fusionada correctament.")
        else:
            print_error("Error en fer el merge de la PR.")

    def tancar_pull_request(self):
        """Tancar una pull request sense merge"""
        nom_repo = input_info("Nom del repo: ")
        pr_number = input_info("Número de la PR a tancar: ")
        resposta = self.gestor_repos.close_pull_request(nom_repo, pr_number)

        if resposta.get("html_url"):
            print_success("Pull request tancada correctament.")
            print_success(f' 🌐 URL: {resposta.get("html_url")}')
        else:
            print_error("Error en tancar la PR.")

    def afegir_colaborador(self):
        """Afegir un col·laborador"""
        nom_repo = input_info("Nom del repo: ")
        col·laborador = input_info("Usuari a afegir: ")
        permís = input_info("Permisos (pull/push/admin): ")

        if self.gestor_repos.add_collaborator(nom_repo, col·laborador, permís):
            print_success("Col·laborador afegit correctament.")
        else:
            print_error("Error en afegir el col·laborador.")

    def llistar_colaboradors(self):
        """Llistar col·laboradors del repo"""
        nom_repo = input_info("Nom del repo: ")
        col·laboradors = self.gestor_repos.list_collaborators(nom_repo)
        print_info("\n=== Col·laboradors ===")
        for col·laborador in col·laboradors:
            print_info(f"- {col·laborador['login']} ({col·laborador['permissions']})")

    def sortir(self):
        """Sortir del menú"""

    def opcio_invalida(self):
        """Opció no vàlida"""
        print_error("Opció no vàlida.")
