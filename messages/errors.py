from .ansi_escape_codes import *

def perm_denied(role):
    return f"En tant que membre de l'equipe {role}, vous n'avez pas le droit de faire cette action."

def wrong_team(team):
    msg = (
        f"{BOLD}{RED}L'équipe {team} n'existe pas.{RESET}"
        f"Choisir parmi '{MAGENTA}gestion{RESET}', '{CYAN}support{RESET}', et '{GREEN}commercial{RESET}'."
    )
    return msg