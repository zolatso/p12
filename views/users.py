import rich_click as click

from .errors import perm_denied
from .decorators import requires
from db.crud import create_user, get_usernames, get_specific_user

@click.group()
@click.pass_context
def user_group(ctx):
    """User commands"""

@user_group.command()
@click.pass_context
@requires("read a resource")
def show(ctx):
    all_users = get_usernames()
    click.echo("Veuillez choisir un utilisateur dans la liste de tous les utilisateurs (entrez le numero)")
    for i, option in enumerate(all_users, start=1):
        click.echo(f"{i}. {option}")
    choice_num = click.prompt(
        "Enter the number of your choice",
        type=click.IntRange(1, len(all_users))
    )
    selected_user = all_users[choice_num - 1]
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
@click.argument("name")
@click.pass_context
def delete(ctx, name):
    pass