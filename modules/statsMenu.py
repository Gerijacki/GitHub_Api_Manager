from modules.utils import print_warning, print_error, print_info, print_success, clear_screen, pause, input_warning, input_info
# ================== GESTIÓ D'ESTADÍSTIQUES DEL REPO ================== #
class StatsMenu:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager
    
    def ver_stats_repo(self):
        owner = input_info("Propietari del repo: ")
        repo_name = input_info("Nom del repo: ")

        while True:
            clear_screen()
            print_info(f"\n=== Estadístiques del repo: {repo_name} ===")
            print_info("1. Resum general")
            print_info("2. Commits recents")
            print_info("3. Branques del repo")
            print_info("4. Releases del repo")
            print_info("5. Issues obertes")
            print_info("6. Pull requests obertes")
            print_info("7. Tornar al menú principal")

            opcion = input_info("\nSel·lecciona una opció: ")

            if opcion == "1":
                stats = self.stats_manager.get_repo_overview(owner, repo_name)
                print_info("\n=== Resum del repo ===")
                for key, value in stats.items():
                    print_info(f"{key}: {value}")

            elif opcion == "2":
                commits = self.stats_manager.get_repo_commits(owner, repo_name)
                print_info("\n=== Últims commits ===")
                for commit in commits[:15]:
                    print_info(
                        f"- {commit['commit']['message']} ({commit['commit']['author']['name']})"
                    )

            elif opcion == "3":
                branches = self.stats_manager.get_repo_branches(owner, repo_name)
                print_info("\n=== Branques del repo ===")
                for branch in branches:
                    print_info(f"- {branch['name']}")

            elif opcion == "4":
                releases = self.stats_manager.get_repo_releases(owner, repo_name)
                print_info("\n=== Releases del repo ===")
                for release in releases:
                    print_info(f"- {release['name']} (Tag: {release['tag_name']})")

            elif opcion == "5":
                issues = self.stats_manager.get_repo_issues(owner, repo_name)
                print_info("\n=== Issues Obertes ===")
                for issue in issues:
                    print_info(
                        f"- #{issue['number']} {issue['title']} (Estado: {issue['state']})"
                    )

            elif opcion == "6":
                prs = self.stats_manager.get_repo_pull_requests(owner, repo_name)
                print_info("\n=== Pull Requests Obertes ===")
                for pr in prs:
                    print_info(f"- #{pr['number']} {pr['title']} ({pr['state']})")

            elif opcion == "7":
                break

            else:
                print_info("\nOpció no vàlida.")

            pause()
