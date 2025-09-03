import rich_click as click

from .ansi_escape_codes import *
from .decorators import framed

def confirm_delete(name):
    return f"{BOLD}{RED}Est-ce que vous etes sur de vouloir supprimer {RESET}{CYAN}'{name}' 😱? {RESET}"

def deletion_avoided(name):
    return f"{name} n'a pas été supprimé."

logout_success = f"{BOLD}{MAGENTA}Vous vous êtes déconnecté avec succès.{RESET}"

login_required = (
    f"{BOLD}{RED}Vous n'êtes pas connecté ! {RESET}\n"
    "Veuillez saisir votre adresse e-mail"
)

def display_user(name, email, role):
    click.echo(f"{BOLD}{CYAN}{'-'*30}{RESET}")
    click.echo(f"{BOLD}{CYAN}🧑 Informations sur l’employé 🧑{RESET}")
    click.echo(f"{MAGENTA}Nom: {BOLD}{name}{RESET}")
    click.echo(f"{YELLOW}Mail: {BOLD}{email}{RESET}")
    click.echo(f"{GREEN}Role: {BOLD}{role}{RESET}")
    click.echo(f"{BOLD}{CYAN}{'-'*30}{RESET}")

@framed
def create_welcome(user, object):
    return f"Bonjour {user}, vous allez créer un nouveau {object}."