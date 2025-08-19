import rich_click as click

from .decorators import requires
from .helpers import prompt_from_list, user_from_list_or_argument
from db.create import create_user
from db.read import get_specific_user
from db.delete import delete_specific_user
from db.update import update_user


@click.group()
@click.pass_context
def user_group(ctx):
    """User commands"""

@user_group.command()
@click.argument("username", required=False)
@click.pass_context
@requires("read a resource")
def show(ctx, username):
    selected_user = user_from_list_or_argument(username)
    user = get_specific_user(selected_user)
    click.echo(f"Nom: {user["name"]}")
    click.echo(f"Email: {user["email"]}")
    click.echo(f"Role: {user["role"]}")
    

@user_group.command()
@click.pass_context
@requires("create user")
def add(ctx):
    user = ctx.obj["name"]
    click.echo(f"Bonjour {user}, vous allez créer un nouveau collaborateur.")
    name = click.prompt("Prénom et nom du collaborateur")
    email = click.prompt("Email du collaborateur")
    password = click.prompt("Mot de passe pour le collaborateur")
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
        click.echo(f"Unexpected error: {e}")
    
@user_group.command()
@click.argument("username", required=False)
@click.pass_context
@requires("delete user")
def delete(ctx, username):
    selected_user = user_from_list_or_argument(username)
    if click.confirm(f"Est-ce que vous etes sur de vouloir supprimer '{selected_user}'?", default=False):
        # Do the deletion here
        click.echo(f"{selected_user} a été supprimé.")
        # Should be in a try
        try:
            delete_specific_user(selected_user)
        except Exception as e:
            click.echo(f"Unexpected error: {e}")
    else:
        click.echo(f"{selected_user} n'a pas été supprimé.")

@user_group.command()
@click.argument("username", required=False)
@click.pass_context
@requires("update user")
def update(ctx, username):
    selected_user = user_from_list_or_argument(username)
    user = get_specific_user(selected_user)

    selected_field = prompt_from_list(
        "Veuillez choisir le champ que vous voudriez modifier",
        user.values()
    )
    
    selected_field_name = [field_name for field_name, val in user.items() if val == selected_field][0]

    if selected_field_name == "role":
        modification = click.prompt(
            f"Choisir le nouveau role pour {selected_user}",
            type=click.Choice(["gestion", "commercial", "support"], case_sensitive=False)
        )
    else:
        modification = click.prompt(
            f"Entrez le nouveau {selected_field_name} pour {selected_user}"
        )
    try:
        update_user(selected_user, selected_field_name, modification)
        click.echo(f"Le {selected_field_name} de {selected_user} a été modifié.")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")        
