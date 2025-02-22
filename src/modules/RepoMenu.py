from src.modules.Utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info

class RepoMenu:
    def __init__(self, gestor_repos):
        self.gestor_repos = gestor_repos
        self.opcions_menu = {
            "1": self.llistar_repositoris,
            "2": self.crear_repositori,
            "3": self.eliminar_repositori,
            "4": self.llistar_branques,
            "5": self.crear_branques,
            "6": self.eliminar_branques,
            "7": self.fusionar_branques,
            "8": self.llistar_pull_requests,
            "9": self.crear_pull_request,
            "10": self.fer_merge_pull_request,
            "11": self.tancar_pull_request,
            "12": self.llistar_colaboradors,
            "13": self.afegir_colaborador,
            "14": self.sortir
        }

    def gestionar_repo(self):
        while True:
            clear_screen()
            print_info("\n=== Gestió dels repositoris ===")
            for key, action in self.opcions_menu.items():
                print_info(f"{key}. {action.__doc__}")
            
            opcio = input_info("\nSelecciona una opció: ")
            if opcio == "14":
                return
            
            self.opcions_menu.get(opcio, self.opcio_invalida)()

            pause()

    def crear_repositori(self):
        """Crear un repositori"""
        nom = input_info("Nom del nou repo: ")
        if not nom.strip():
            print_error("El nom del repositori no pot estar buit.")
            return
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
    
    def llistar_repositoris(self):
        """Llistar repos (propietari o col·laborador)"""
        repos = self.gestor_repos.list_repos()

        if isinstance(repos, dict) and "error" in repos:
            print_error(f"Error obtenint repos: {repos['error']}")
            return

        repos_filtrats = [repo for repo in repos if repo.get("permissions", {}).get("push", False)]

        if repos_filtrats:
            print_info("\n=== Repositoris del teu compte ===")
            for idx, repo in enumerate(repos_filtrats, 1):
                tipus = "🔒 Privat" if repo["private"] else "🌍 Públic"
                print_info(f"{idx}. {repo['name']} ({tipus})")
        else:
            print_error("No s'han trobat repositoris propietaris o editables.")

    def seleccionar_repositori(self):
        """Seleccionar un repositori del llistat"""
        repos = self.gestor_repos.list_repos()
        if repos:
            print_info("\nSelecciona un repositori:")
            for idx, repo in enumerate(repos, 1):
                print_info(f"{idx}. {repo['name']}")
            
            try:
                seleccio = int(input_info("\nIntrodueix el número del repositori: "))
                if 1 <= seleccio <= len(repos):
                    selected_repo = repos[seleccio - 1]
                    print_success(f"Repositori seleccionat: {selected_repo['name']}")
                    return selected_repo['name']
                else:
                    print_error("Selecció no vàlida.")
            except ValueError:
                print_error("Selecciona un número vàlid.")
        else:
            print_error("No s'han trobat repositoris.")

    def eliminar_repositori(self):
        """Eliminar un repositori"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
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
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            branques = self.gestor_repos.list_branches(nom_repo)
            if isinstance(branques, list):
                if branques:
                    print_info("\n=== Branques del repositori ===")
                    for branca in branques:
                        if isinstance(branca, dict) and "name" in branca:
                            print_info(f"- {branca['name']}")
                        else:
                            print_warning("Es va rebre una branca mal formatada.")
                else:
                    print_error("No s'han trobat branques o hi ha un error.")
            else:
                print_error(f"Error: {branques.get('error', 'Error desconegut')}")


    def crear_branques(self):
        """Crear una nova branca"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            nova_branque = input_info("Nom de la nova branca: ")
            if not nova_branque.strip():
                print_error("El nom de la branca no pot estar buit.")
                return
            branca_base = input_info("Branca base (per defecte 'main'): ") or "main"

            resposta = self.gestor_repos.create_branch(nom_repo, nova_branque, branca_base)
            if resposta.get("url"):
                print_success("Branca creada correctament.")
            else:
                print_error("Error en crear la branca.")

    def eliminar_branques(self):
        """Eliminar una branca"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            nom_branque = input_warning("Nom de la branca a eliminar: ")
            if not nom_branque.strip():
                print_error("El nom de la branca no pot estar buit.")
                return
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
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            head = input_info("Branca origen: ")
            base = input_info("Branca destí: ")
            if not head.strip() or not base.strip():
                print_error("El nom de les branques no pot estar buits.")
                return
            resposta = self.gestor_repos.merge_branches(nom_repo, base, head)
            if resposta and isinstance(resposta, dict):
                message = resposta.get("commit", {}).get("message", "No message returned")
                html_url = resposta.get("html_url", "No URL available")

                print_success(f"Merge completat de {head} cap a {base}")
                print_success(f"🌐 URL: {html_url}")
                print_success(f"🚀 Commit message: {message}")
            else:
                print_error("Resposta no vàlida. Revisa la resposta de GitHub.")

    def crear_pull_request(self):
        """Crear una pull request"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            titol = input_info("Títol de la PR: ")
            head = input_info("Branca d'origen: ")
            base = input_info("Branca de destí (per defecte 'main'): ") or "main"
            cos = input_info("Descripció de la PR: ")

            resposta = self.gestor_repos.create_pull_request(nom_repo, titol, head, base, cos)
            
            if resposta and isinstance(resposta, dict):
                pr_number = resposta.get("number")
                pr_url = resposta.get("html_url", "No URL available")
                
                if pr_number:
                    print_success("✅ PR creada correctament.")
                    print_info(f"🆔 ID: {pr_number}")
                    print_info(f"🔗 URL: {pr_url}")
                else:
                    print_error("⚠️ Error en crear la PR. Verifica les dades introduïdes.")
            else:
                print_error("❌ Resposta no vàlida. Revisa la resposta de GitHub.")

    def llistar_pull_requests(self):
        """Llistar pull requests obertes"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            prs = self.gestor_repos.list_pull_requests(nom_repo)
            print_info("\n=== Pull Requests Obertes ===")
            
            if isinstance(prs, list):
                for pr in prs:
                    if isinstance(pr, dict):
                        print_info(f"- #{pr['number']} {pr['title']} ({pr['state']})")
                    else:
                        print_warning("PR mal formatada detectada.")
            else:
                print_error("No s'han trobat PR obertes o hi ha un error amb la resposta.")


    def fer_merge_pull_request(self):
        """Fer merge d'una pull request"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            pr_number = input_info("Número de la PR a fusionar: ")
            if not pr_number.isdigit():
                print_error("Introduïu un número vàlid per la PR.")
                return
            resposta = self.gestor_repos.merge_pull_request(nom_repo, pr_number)

            if resposta.get("merged"):
                print_success("Pull request fusionada correctament.")
            else:
                print_error("Error en fer el merge de la PR.")

    def tancar_pull_request(self):
        """Tancar una pull request sense merge"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            pr_number = input_info("Número de la PR a tancar: ")
            if not pr_number.isdigit():
                print_error("Introduïu un número vàlid per la PR.")
                return
            resposta = self.gestor_repos.close_pull_request(nom_repo, pr_number)

            if resposta.get("html_url"):
                print_success("Pull request tancada correctament.")
                print_success(f' 🌐 URL: {resposta.get("html_url")}')
            else:
                print_error("Error en tancar la PR.")

    def afegir_colaborador(self):
        """Afegir un col·laborador"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            collaborador = input_info("Usuari a afegir: ")
            permís = input_info("Permisos (pull/push/admin): ")

            if self.gestor_repos.add_collaborator(nom_repo, collaborador, permís):
                print_success("Col·laborador afegit correctament.")
            else:
                print_error("Error en afegir el col·laborador.")

    def llistar_colaboradors(self):
        """Llistar col·laboradors del repo"""
        nom_repo = self.seleccionar_repositori()
        if nom_repo:
            collaboradors = self.gestor_repos.list_collaborators(nom_repo)
            print_info("\n=== Col·laboradors ===")
            for collaborador in collaboradors:
                print_info(f"- {collaborador['login']} ({collaborador['permissions']})")

    def sortir(self):
        """Sortir del menú"""

    def opcio_invalida(self):
        """Opció no vàlida"""
        print_error("Opció no vàlida.")
