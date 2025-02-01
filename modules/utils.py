import os

# ================== CONFIGURACIÓN DE COLORES ================== #
class Utils:
    SUCCESS = "\033[92m"  # Verde
    ERROR = "\033[91m"  # Rojo
    WARNING = "\033[93m"  # Amarillo
    INFO = "\033[94m"  # Azul
    RESET = "\033[0m"  # Reset

# ================== FUNCIONES DE IMPRESIÓN ================== #
def print_success(message):
    print(f"{Utils.SUCCESS}[ ✔ ] {message}{Utils.RESET}")

def print_error(message):
    print(f"{Utils.ERROR}[ ✖ ] {message}{Utils.RESET}")

def print_warning(message):
    print(f"{Utils.WARNING}[ ⚠ ] {message}{Utils.RESET}")

def print_info(message):
    print(f"{Utils.INFO} {message}{Utils.RESET}")

def input_success(message):
    return input(f"{Utils.SUCCESS}[ ✔ ] {message}: {Utils.RESET}")

def input_error(message):
    return input(f"{Utils.ERROR}[ ✖ ] {message}: {Utils.RESET}")

def input_warning(message):
    return input(f"{Utils.WARNING}[ ⚠ ] {message}: {Utils.RESET}")

def input_info(message):
    return input(f"{Utils.INFO} {message}: {Utils.RESET}")

# ================== UTILIDADES GENERALES ================== #
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def pause():
    input("Presiona Enter para continuar...")