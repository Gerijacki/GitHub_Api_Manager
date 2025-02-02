from modules.Utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info

class StatsMenu:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager

    def ver_stats_repo(self):
        """Menú de visualització d'estadístiques d'un repositori"""
        owner = input_info("Propietari del repo: ")
        repo_name = input_info("Nom del repo: ")

        menu_options = {
            "1": self.mostrar_resum_repo,
            "2": self.mostrar_commits_recents,
            "3": self.mostrar_branques_repo,
            "4": self.mostrar_releases_repo,
            "5": self.mostrar_issues_obertes,
            "6": self.mostrar_pull_requests,
            "7": self.sortir
        }

        while True:
            clear_screen()
            print_info(f"\n=== Estadístiques del repo: {repo_name} ===")
            for key in menu_options.items():
                print_info(f"{key}. {key.__doc__}")

            opcion = input_info("\nSel·lecciona una opció: ")
            if opcion == "7":
                return

            func = menu_options.get(opcion, (self.opcio_invalida,))[0]
            func(owner, repo_name)
            pause()

    def mostrar_resum_repo(self, owner, repo_name):
        """Resum general del repositori"""
        stats = self.stats_manager.get_repo_overview(owner, repo_name)
        print_info("\n=== Resum del repo ===")
        for key, value in stats.items():
            print_info(f"{key}: {value}")

    def mostrar_commits_recents(self, owner, repo_name):
        """Últims commits del repositori"""
        commits = self.stats_manager.get_repo_commits(owner, repo_name)
        print_info("\n=== Últims commits ===")
        for commit in commits[:15]:
            print_info(f"- {commit['commit']['message']} ({commit['commit']['author']['name']})")

    def mostrar_branques_repo(self, owner, repo_name):
        """Branques del repositori"""
        branches = self.stats_manager.get_repo_branches(owner, repo_name)
        print_info("\n=== Branques del repo ===")
        for branch in branches:
            print_info(f"- {branch['name']}")

    def mostrar_releases_repo(self, owner, repo_name):
        """Releases del repositori"""
        releases = self.stats_manager.get_repo_releases(owner, repo_name)
        print_info("\n=== Releases del repo ===")
        for release in releases:
            print_info(f"- {release['name']} (Tag: {release['tag_name']})")

    def mostrar_issues_obertes(self, owner, repo_name):
        """Issues obertes del repositori"""
        issues = self.stats_manager.get_repo_issues(owner, repo_name)
        print_info("\n=== Issues Obertes ===")
        for issue in issues:
            print_info(f"- #{issue['number']} {issue['title']} (Estat: {issue['state']})")

    def mostrar_pull_requests(self, owner, repo_name):
        """Pull requests obertes del repositori"""
        prs = self.stats_manager.get_repo_pull_requests(owner, repo_name)
        print_info("\n=== Pull Requests Obertes ===")
        for pr in prs:
            print_info(f"- #{pr['number']} {pr['title']} ({pr['state']})")

    def sortir(self, owner=None, repo_name=None):
        """Sortir del menú"""
        return

    def opcio_invalida(self, owner=None, repo_name=None):
        """Opció no vàlida"""
        print_error("Opció no vàlida.")
