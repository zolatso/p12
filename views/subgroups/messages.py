from .helper_functions.ansi_escape_codes import *

def confirm_delete(name):
    return f"{BOLD}{RED}Est-ce que vous etes sur de vouloir supprimer {RESET}{CYAN}'{name}'? {RESET}"

def deletion_avoided(name):
    return f"{name} n'a pas été supprimé."