import os
# ================== GESTIÓ D'ESTADÍSTIQUES DEL REPO ================== #
class StatsMenu:
    def __init__(self, stats_manager):
        self.stats_manager = stats_manager
    
    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input("Prem Enter per continuar...")
def ver_stats_repo(self):
    owner = input("Propietari del repo: ")
    repo_name = input("Nom del repo: ")

    while True:
        self.clear_screen()
        print(f"\n=== Estadístiques del repo: {repo_name} ===")
        print("1. Resum general")
        print("2. Commits recents")
        print("3. Branques del repo")
        print("4. Releases del repo")
        print("5. Issues obertes")
        print("6. Pull requests obertes")
        print("7. Tornar al menú principal")

        opcion = input("\nSel·lecciona una opció: ")

        if opcion == "1":
            stats = self.stats_manager.get_repo_overview(owner, repo_name)
            print("\n=== Resum del repo ===")
            for key, value in stats.items():
                print(f"{key}: {value}")

        elif opcion == "2":
            commits = self.stats_manager.get_repo_commits(owner, repo_name)
            print("\n=== Últims commits ===")
            for commit in commits[:15]:
                print(
                    f"- {commit['commit']['message']} ({commit['commit']['author']['name']})"
                )

        elif opcion == "3":
            branches = self.stats_manager.get_repo_branches(owner, repo_name)
            print("\n=== Branques del repo ===")
            for branch in branches:
                print(f"- {branch['name']}")

        elif opcion == "4":
            releases = self.stats_manager.get_repo_releases(owner, repo_name)
            print("\n=== Releases del repo ===")
            for release in releases:
                print(f"- {release['name']} (Tag: {release['tag_name']})")

        elif opcion == "5":
            issues = self.stats_manager.get_repo_issues(owner, repo_name)
            print("\n=== Issues Obertes ===")
            for issue in issues:
                print(
                    f"- #{issue['number']} {issue['title']} (Estado: {issue['state']})"
                )

        elif opcion == "6":
            prs = self.stats_manager.get_repo_pull_requests(owner, repo_name)
            print("\n=== Pull Requests Obertes ===")
            for pr in prs:
                print(f"- #{pr['number']} {pr['title']} ({pr['state']})")

        elif opcion == "7":
            break

        else:
            print("\nOpció no vàlida.")

        self.pause()
