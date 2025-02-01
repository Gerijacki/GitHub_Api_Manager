import sys
from menu import Menu
from modules.utils import print_warning

if __name__ == "__main__":
    try:
        menu = Menu()
        menu.mostrar_menu()
    except KeyboardInterrupt:
        print_warning("\n\nS'ha interromput l'execució amb Ctrl+C. Sortint...")
        sys.exit(0)

