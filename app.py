import sys
from menu import Menu

if __name__ == "__main__":
    try:
        menu = Menu()
        menu.mostrar_menu()
    except KeyboardInterrupt:
        print("\n\n❌ S'ha interromput l'execució amb Ctrl+C. Sortint...")
        sys.exit(0)

