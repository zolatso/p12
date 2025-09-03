import rich_click as click

from .helper_functions.ansi_escape_codes import *
from .helper_functions.decorators import requires
from .helper_functions.helpers import prompt_from_list, user_from_list_or_argument, get_selected_field
from .helper_functions.validators import valid_email, valid_string, valid_password
from db.create import create_user
from db.read import get_specific_user
from db.delete import delete_specific_user
from db.update import update_user


@click.group()
@click.pass_context
def user_group(ctx):
    """User commands"""

@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez voir")
@click.option("--equipe", help="Le nom de l'equipe dont vous voudriez voir les membres")
@click.option("--self", is_flag=True, help="Pour voir vos propres coordonnées")
@click.pass_context
@requires("read a resource")
def show(ctx, nom):
    selected_user = user_from_list_or_argument(nom)
    user = get_specific_user(selected_user)
    click.echo(f"{BOLD}{CYAN}🧑 Informations sur l’employé 🧑{RESET}")
    click.echo(f"{MAGENTA}Nom: {BOLD}{user['name']}{RESET}")
    click.echo(f"{YELLOW}Mail: {BOLD}{user['email']}{RESET}")
    click.echo(f"{GREEN}Role: {BOLD}{user['role']}{RESET}")
    click.echo(f"{BOLD}{CYAN}{'-'*30}{RESET}")

@user_group.command()
@click.pass_context
@requires("create user")
def add(ctx):
    user = ctx.obj["name"]
    click.echo(f"Bonjour {user}, vous allez créer un nouveau collaborateur.")
    name = valid_string(50, "Prénom et nom du collaborateur")
    email = valid_email()
    password = valid_password()
    role = click.prompt(
        "Leur role",
        type=click.Choice(["gestion", "commercial", "support"], case_sensitive=False)
    )
    try:
        create_user(
            name,
            email,
            password,
            role
        )
    except Exception as e:
        click.ClickException(f"Erreur: {e}")
    
@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez supprimer")
@click.pass_context
@requires("delete user")
def delete(ctx, nom):
    selected_user = user_from_list_or_argument(nom)
    if click.confirm(f"Est-ce que vous etes sur de vouloir supprimer '{selected_user}'?", default=False):
        # Do the deletion here
        click.echo(f"{selected_user} a été supprimé.")
        # Should be in a try
        try:
            delete_specific_user(selected_user)
        except Exception as e:
            click.ClickException(f"Erreur: {e}")
    else:
        click.echo(f"{selected_user} n'a pas été supprimé.")

@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez supprimer")
@click.pass_context
@requires("update user")
def update(ctx, nom):
    selected_user = user_from_list_or_argument(nom)
    user = get_specific_user(selected_user)
    selected_field = get_selected_field(user)

    match selected_field:
        case "role":
            modification = click.prompt(
                f"Choisir le nouveau role pour {selected_user}",
                type=click.Choice(["gestion", "commercial", "support"], case_sensitive=False)
            )
        case "name":
            modification = valid_string(100, f"Entrez le nouveau nom pour {selected_user}")
        case "email":
            modification = valid_email()
    try:
        update_user(selected_user, selected_field, modification)
        click.echo(f"Le {selected_field} de {selected_user} a été modifié.")
    except Exception as e:
        click.echo(f"Erreur: {e}")        
