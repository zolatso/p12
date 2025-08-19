import click

from .decorators import requires
from .helpers import client_from_list_or_argument, prompt_from_list
from db.create import create_client
from db.read import get_specific_client
from db.update import update_client


@click.group()
@click.pass_context
def client_group(ctx):
    """User commands"""

@client_group.command()
@click.argument("client_name", required=False)
@click.pass_context
@requires("read a resource")
def show(ctx, client_name):
    selected_client = client_from_list_or_argument(client_name)
    client = get_specific_client(selected_client)
    for k, v in client.items():
        click.echo(f"{k}: {v}")

@client_group.command()
@click.pass_context
@requires("create client")
def add(ctx):
    user = ctx.obj["name"]
    click.echo(f"Bienvenu, {user}. Vous allez ajouter un nouveau client.")
    fullname = click.prompt("Nom et prenom du client")
    email = click.prompt("Email")
    phone = click.prompt("Numero de telephone")
    business_name = click.prompt("Nom de l'entreprise")
    # Creation date is manually input in case the commercial has developed relationship previously
    created_at = click.prompt("Premier contact avec le client (dd/mm/yyyy)")
    # For new creation of clients, updated_at can just be datetime.now so we don't send this arg
    try:
        create_client(
            user,
            fullname,
            email,
            phone,
            business_name,
            created_at
        )
    except Exception as e:
        click.echo(f"Unexpected error: {e}")

@client_group.command()
@click.argument("client_name", required=False)
@click.pass_context
@requires("update client")
def update(ctx, client_name):
    selected_client = client_from_list_or_argument(client_name)
    client = get_specific_client(selected_client)

    # Extra permission required here: only the commercial associated with a specific client can update them.
    user = ctx.obj["name"]
    associated_commercial = client["user"]
    if not user == associated_commercial:
        raise click.ClickException(
            f"""Vous n'êtes pas le commercial associé à ce client, vous ne pouvez donc pas modifier ses coordonnées.
            Veuillez contacter {associated_commercial}, qui est son représentant."""
            )

    selected_field = prompt_from_list(
        "Veuillez choisir le champ que vous voudriez modifier",
        client.values()
    )
    
    selected_field_name = [field_name for field_name, val in client.items() if val == selected_field][0]

    if selected_field_name == "role":
        modification = click.prompt(
            f"Choisir le nouveau role pour {selected_client}",
            type=click.Choice(["gestion", "commercial", "support"], case_sensitive=False)
        )
    else:
        modification = click.prompt(
            f"Entrez le nouveau {selected_field_name} pour {selected_client}"
        )
    try:
        update_client(selected_client, selected_field_name, modification)
        click.echo(f"Le {selected_field_name} de {selected_client} a été modifié.")
    except Exception as e:
        click.echo(f"Unexpected error: {e}")   







    