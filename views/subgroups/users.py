import rich_click as click

from ..helper_functions.decorators import requires
from ..helper_functions.helpers import prompt_from_list, user_from_list_or_argument, get_selected_field
from ..helper_functions.validators import valid_email, valid_string, valid_password

from messages.messages import confirm_delete, deletion_avoided, display_user, create_welcome
from messages.errors import wrong_team
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
def show(ctx, nom, equipe, self):
    """
    La fonctionnalité d'affichage pour le groupe d'utilisateurs. Elle propose trois options : 
    nom (indiquez directement l'utilisateur que vous souhaitez voir), équipe (choisissez une équipe particulière 
    à consulter) et soi (une valeur booléenne pour voir vos propres détails).
    """

    # Check if user wants to see their own details
    if not self:
        # Check if team option has been set/passed
        if equipe and equipe not in ['commercial','support','gestion']:
            raise click.ClickException(wrong_team(equipe))
        if not equipe:
            equipe = "all"
        selected_user = user_from_list_or_argument(nom, equipe)
    else:
        selected_user = ctx.obj["name"]

    user = get_specific_user(selected_user)

    display_user(user['name'], user['email'], user['role'])



@user_group.command()
@click.pass_context
@requires("create user")
def add(ctx):
    """
    Permet la création d'un nouvel utilisateur. 
    Vérifie les autorisations, puis demande les informations nécessaires.
    """
    user = ctx.obj["name"]
    click.echo(create_welcome(user, "collaborateur"))

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
    equipe = "all"
    selected_user = user_from_list_or_argument(nom, equipe)

    if click.confirm(confirm_delete(selected_user), default=False):
        # Do the deletion here
        click.echo(f"{selected_user} a été supprimé.")
        # Should be in a try
        try:
            delete_specific_user(selected_user)
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
    equipe = "all"
    selected_user = user_from_list_or_argument(nom, equipe)
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
