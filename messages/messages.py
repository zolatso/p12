import rich_click as click
import random

from .ansi_escape_codes import *
from .decorators import framed


def confirm_delete(name):
    return f"{BOLD}{RED}Est-ce que vous etes sur de vouloir supprimer {RESET}{CYAN}'{name}' 😱? {RESET}"


def deletion_avoided(name):
    return f"{name} n'a pas été supprimé."


def deletion_successful(name):
    return f"{name} a été supprimé."


@framed
def modification_success(field, name):
    msg = (
        f"\n{BOLD}Super !{RESET} Le {BOLD}{random.choice(color_list)}{field}{RESET} "
        f"de {random.choice(color_list)}{name}{RESET} a été modifié avec succès.\n"
    )
    return msg


logout_success = f"{BOLD}{MAGENTA}Vous vous êtes déconnecté avec succès.{RESET}"

login_required = (
    f"{BOLD}{RED}Vous n'êtes pas connecté ! {RESET}\n"
    "Veuillez saisir votre adresse e-mail"
)


def display_user(user):
    click.echo()
    click.echo(f"{BOLD}{CYAN}{'-' * 30}{RESET}")
    click.echo(f"{BOLD}{CYAN}🧑 Informations sur l’employé 🧑{RESET}")
    click.echo(f"{MAGENTA}Nom: {BOLD}{user['name']}{RESET}")
    click.echo(f"{YELLOW}Mail: {BOLD}{user['email']}{RESET}")
    click.echo(f"{GREEN}Role: {BOLD}{user['role']}{RESET}")
    click.echo(f"{BOLD}{CYAN}{'-' * 30}{RESET}")
    click.echo()


def display_client(client):
    click.echo()
    click.echo(f"{BOLD}{CYAN}{'-' * 33}{RESET}")
    click.echo(f"{BOLD}{CYAN}🧑 Informations sur le client 🧑{RESET}")

    for k, v in client.items():
        if isinstance(v, str):
            click.echo(
                f"{BOLD}{random.choice(color_list)}{k}{RESET}: {random.choice(color_list)}{v}{RESET}"
            )
        if isinstance(v, list):
            click.echo(f"{BOLD}{random.choice(color_list)}{k}{RESET}:")
            for item in v:
                click.echo(f"{random.choice(color_list)}{item}{RESET}, ")

    click.echo(f"{BOLD}{CYAN}{'-' * 33}{RESET}")
    click.echo()


def display_contracts(contracts):
    for index, contract in enumerate(contracts):
        click.echo()
        click.echo(f"CONTRAT {index + 1}")
        click.echo("-" * 50)
        if "event" in contract:
            title = f"Le contrat pour l'evenement: {BOLD}{random.choice(color_list)}{contract['event']}{RESET}"
        else:
            title = f"{random.choice(color_list)}Ce contrat n'a toujours pas d'evenement.{RESET}"
        click.echo(title)
        click.echo()
        click.echo(
            f"{BOLD}{random.choice(color_list)}Valeur du contrat:{RESET} {contract['total_amount']}"
        )
        click.echo(
            f"{BOLD}{random.choice(color_list)}Montant non payé:{RESET} {contract['amount_remaining']}"
        )
        click.echo(
            f"{BOLD}{random.choice(color_list)}Commercial associé avec ce contrat:{RESET} {contract['associated_commercial']}"
        )
        click.echo(
            f"{BOLD}{random.choice(color_list)}Crée le:{RESET} {contract['created_at']}"
        )
        if contract["is_signed"]:
            is_signed = "Ce contrat a été signé"
        else:
            is_signed = "Ce contrat n'a toujours pas été signé"
        click.echo()
        click.echo(is_signed)
        click.echo("-" * 50)


@framed
def display_event(event):
    click.echo()
    for k, v in event.items():
        click.echo(f"{BOLD}{random.choice(color_list)}{k}{RESET}: {v}")
    click.echo()


@framed
def welcome(user, action, object):
    msg = (
        f"\nBonjour {BOLD}{MAGENTA}{user}{RESET}, vous allez {BOLD}{CYAN}{action}{RESET} "
        f"un {BOLD}{RED}{object}{RESET}.\n"
    )
    return msg


def list_options(number, option):
    msg = f"{BOLD}{random.choice(color_list)}{number}. {random.choice(color_list)}{option}{RESET}"
    return msg


def choose_msg(object):
    return f"Veuillez choisir un {BOLD}{random.choice(color_list)}{object}{RESET}:\n"


@framed
def success(action, object):
    msg = (
        f"\n{BOLD}Super !{RESET} Vous avez {BOLD}{random.choice(color_list)}{action}{RESET} "
        f"un {BOLD}{random.choice(color_list)}{object}{RESET} avec succès.\n"
    )
    return msg
