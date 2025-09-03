import rich_click as click

from .helper_functions.decorators import requires
from .helper_functions.helpers import client_from_list_or_argument, prompt_from_list, get_selected_field
from .helper_functions.validators import valid_email, valid_phone, valid_string, valid_date
from db.create import create_client
from db.read import get_specific_client, get_equipe_usernames
from db.update import update_client

clean_field_names = {
    "name" : "Nom",
    "email" : "Mail",
    "phone" : "Phone",
    "business_name" : "Nom de l'entreprise",
    "created_at" : "Date de creation",
    "updated_at" : "Dernier mise à jour",
    "user" : "Commercial associé",
    "contracts" : "Contracts"
}


@click.group()
@click.pass_context
def client_group(ctx):
    """Client commands"""

@client_group.command()
@click.option("--nom", help="Le nom du client que vous voudriez voir")
@click.option("--self", is_flag=True, help="Pour voir les clients que vous representez (équipe commercial)")
@click.pass_context
@requires("read a resource")
def show(ctx, nom, self):
    # If self is activated, we use the specific functionality of only returning selected clients
    if self:
        if ctx.obj["role"] != "commercial":
            raise click.ClickException(
                "L'option --self sur les clients marche que pour les membres de l'equipe commercial"
                )
        selected_client = client_from_list_or_argument(nom, ctx, restrict_for_commercial=True)
    else:
        selected_client = client_from_list_or_argument(nom, ctx)
    
    client = get_specific_client(selected_client)

    for k, v in client.items():
        click.echo(f"{clean_field_names[k]}: {v}")

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
@click.option("--nom", help="Le nom du client que vous voudriez modifier")
@click.pass_context
@requires("update client")
def update(ctx, nom):
    # This only shows the clients represented by the specific commercial
    selected_client = client_from_list_or_argument(nom, ctx, restrict_for_commercial=True)
    client = get_specific_client(selected_client)
    
    # Here we remove contracts from the fields that can be modified as this doesn't seem like a good idea.
    modifiable_fields = {k: v for k, v in client.items() if k != "contracts"}

    selected_field = get_selected_field(modifiable_fields)

    match selected_field:
        case "user":
            # If user wants to modify the commercial associated with the client, different behavior is required.
            all_commercial = get_equipe_usernames("commercial")
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







    