import rich_click as click

from ..helper_functions.decorators import requires
from ..helper_functions.helpers import user_from_list_or_argument, get_selected_field
from ..helper_functions.validators import valid_email, valid_string, valid_password

from messages.messages import (
    confirm_delete,
    deletion_avoided,
    display_user,
    deletion_successful,
    modification_success,
    welcome,
    success,
)
from messages.errors import wrong_team, user_not_found
from db.create import create_user
from db.read import get_specific_user, get_usernames
from db.delete import delete_specific_user
from db.update import update_user


@click.group()
@click.pass_context
def user_group(ctx):
    """
    Options pour afficher, créer, modifier et supprimer des employés (users).
    Seuls les membres de l’équipe de gestion peuvent créer, modifier et supprimer.
    Les autres équipes peuvent consulter les coordonnées des employés, soit en
    choisissant parmi une liste de noms, soit en saisissant le nom d’un employé
    spécifique avec l’option --nom "Prénom Nom". Vous pouvez aussi specifier un equipe
    (--equipe "equipe") ou voir vos propres coordonnées (--self).
    """


@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez voir")
@click.option("--equipe", help="Le nom de l'equipe dont vous voudriez voir les membres")
@click.option("--self", is_flag=True, help="Pour voir vos propres coordonnées")
@click.pass_context
@requires("read a resource")
def show(ctx, nom, equipe, self):
    """
    La fonctionnalité d'affichage pour le groupe d'utilisateurs. Elle propose trois options :
    --nom (indiquez directement l'utilisateur que vous souhaitez voir), --équipe (choisissez une équipe particulière
    à consulter) et --self (une valeur booléenne pour voir vos propres détails).
    """
    click.echo(welcome(ctx.obj["name"], "afficher", "collaborateur"))
    # Check if user wants to see their own details
    if not self:
        # Check if team option has been set/passed
        if equipe and equipe not in ["commercial", "support", "gestion"]:
            raise click.ClickException(wrong_team(equipe))
        if not equipe:
            equipe = "all"
        # If user has supplied a name, check if it exists
        if nom and nom not in get_usernames():
            raise click.ClickException(user_not_found(nom))
        selected_user = user_from_list_or_argument(nom, equipe)
    else:
        selected_user = ctx.obj["name"]

    user = get_specific_user(selected_user)

    display_user(user)


@user_group.command()
@click.pass_context
@requires("create user")
def add(ctx):
    """
    Permet la création d'un nouvel utilisateur.
    Vérifie les autorisations, puis demande les informations nécessaires.
    """
    user = ctx.obj["name"]
    click.echo(welcome(user, "créez", "collaborateur"))

    name = valid_string(50, "Prénom et nom du collaborateur")
    email = valid_email()
    password = valid_password()
    role = click.prompt(
        "Leur role",
        type=click.Choice(["gestion", "commercial", "support"], case_sensitive=False),
    )
    try:
        create_user(name, email, password, role)
        click.echo(success("crée", "collaborateur"))
    except Exception as e:
        click.ClickException(f"Erreur: {e}")


@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez supprimer")
@click.pass_context
@requires("delete user")
def delete(ctx, nom):
    """
    Fonction permettant de supprimer un utilisateur,
    soit en indiquant son nom, soit en le sélectionnant dans une liste.
    """
    click.echo(welcome(ctx.obj["name"], "supprimer", "collaborateur"))

    equipe = "all"
    selected_user = user_from_list_or_argument(nom, equipe)

    if click.confirm(confirm_delete(selected_user), default=False):
        # Do the deletion here
        click.echo(deletion_successful(selected_user))
        # Should be in a try
        try:
            delete_specific_user(selected_user)
            click.echo(success("supprimé", "collaborateur"))
        except Exception as e:
            click.ClickException(f"Erreur: {e}")
    else:
        click.echo(deletion_avoided(selected_user))


@user_group.command()
@click.option("--nom", help="Le nom de l'utilisateur que vous voudriez supprimer")
@click.pass_context
@requires("update user")
def update(ctx, nom):
    """
    Permet de modifier un utilisateur. Prend une option : nom, pour définir l'utilisateur spécifique à modifier.
    Sinon, affiche une liste de tous les utilisateurs. Vérifie les autorisations et valide les entrées.
    """
    click.echo(welcome(ctx.obj["name"], "modifier", "collaborateur"))
    equipe = "all"
    selected_user = user_from_list_or_argument(nom, equipe)
    user = get_specific_user(selected_user)
    selected_field = get_selected_field(user)

    match selected_field:
        case "role":
            modification = click.prompt(
                f"Choisir le nouveau role pour {selected_user}",
                type=click.Choice(
                    ["gestion", "commercial", "support"], case_sensitive=False
                ),
            )
        case "name":
            modification = valid_string(
                100, f"Entrez le nouveau nom pour {selected_user}"
            )
        case "email":
            modification = valid_email()
    try:
        update_user(selected_user, selected_field, modification)
        click.echo(modification_success(selected_field, selected_user))
    except Exception as e:
        click.echo(f"Erreur: {e}")
