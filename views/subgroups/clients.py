import rich_click as click

from .helper_functions.decorators import requires
from .helper_functions.helpers import client_from_list_or_argument, prompt_from_list, get_selected_field
from .helper_functions.validators import valid_email, valid_phone, valid_string, valid_date
from db.create import create_client
from db.read import get_specific_client, get_commercial_usernames
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
    selected_client = client_from_list_or_argument(client_name, ctx)
    client = get_specific_client(selected_client)
    for k, v in client.items():
        click.echo(f"{k}: {v}")

@client_group.command()
@click.pass_context
@requires("create client")
def add(ctx):
    user = ctx.obj["name"]
    click.echo(f"Bienvenu, {user}. Vous allez ajouter un nouveau client.")
    fullname = valid_string(100, "Prenom et nom client")
    email = valid_email()
    phone = valid_phone()
    business_name = valid_string(100, "Nom de l'entreprise")
    # Creation date is manually input in case the commercial has developed relationship previously
    created_at = valid_date("Premier contact avec le client (dd/mm/yyyy)")
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
    
    # Here we remove contracts from the fields that can be modified as this doesn't seem like a good idea.
    modifiable_fields = {k: v for k, v in client.items() if k != "contracts"}

    selected_field = get_selected_field(modifiable_fields)

    match selected_field:
        case "user":
            # If user wants to modify the commercial associated with the client, different behavior is required.
            all_commercial = get_commercial_usernames()
            # Get rid of the current user who logically must be the commercial currently associated with this client,
            # as they passed the permission check earlier
            selectable_users = [v for v in all_commercial if v != user]
            modification = prompt_from_list(
                "Veuillez choisir le commercial que vous voudriez associé à ce client",
                selectable_users
            )
        case "fullname":
            modification = valid_string(100, "Le nouveau nom pour le client")
        case "phone":
            modification = valid_phone()
        case "email":
            modification = valid_email()
        case "business_name":
            modification = valid_string(100, "Le nouveau nom pour l'entreprise du client")
        case "created_at":
            modification = valid_date("Date du premier contact")
        case "updated_at":
            modification = valid_date("Date du dernier contact") 
    try:
        update_client(selected_client, selected_field, modification)
        click.echo(f"Le {selected_field} de {selected_client} a été modifié.")
    except Exception as e:
        click.ClickException(f"Unexpected error: {e}")


@client_group.command()
@click.argument("client_name", required=False)
@click.pass_context
def delete(ctx, client_name):
    # Delete client permission has not been created in db and is not mentioned in cahier des charges
    pass







    