import sys
from src.menu import Menu
from src.modules.Utils import print_warning

if __name__ == "__main__":
    try:
        menu = Menu()
        menu.mostrar_menu()
    except KeyboardInterrupt:
        print_warning("\n\nS'ha interromput l'execució amb Ctrl+C. Sortint...")
        sys.exit(0)

