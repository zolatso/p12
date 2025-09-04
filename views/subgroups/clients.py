import rich_click as click

from ..helper_functions.decorators import requires
from ..helper_functions.helpers import (
    client_from_list_or_argument,
    prompt_from_list,
    get_selected_field,
)
from ..helper_functions.validators import (
    valid_email,
    valid_phone,
    valid_string,
    valid_date,
)
from db.create import create_client
from db.read import get_specific_client, get_equipe_usernames
from db.update import update_client
from messages.messages import (
    modification_success,
    welcome,
    success,
    display_client,
    choose_msg,
)

clean_field_names = {
    "name": "Nom",
    "email": "Mail",
    "phone": "Phone",
    "business_name": "Nom de l'entreprise",
    "created_at": "Date de creation",
    "updated_at": "Dernier mise à jour",
    "user": "Commercial associé",
    "contracts": "Contrats",
}


@click.group()
@click.pass_context
def client_group(ctx):
    """
    Options pour afficher, créer, et modifier des clients.
    Seuls les membres de l’équipe commercial peuvent créer et modifier.
    Les autres équipes peuvent consulter les coordonnées des clients, soit en
    choisissant parmi une liste de noms, soit en saisissant le nom d’un client
    spécifique avec l’option --nom "Prénom Nom". Les membres de l'équipe commerciale peuvent
    consulter les clients qu'ils représentent en ajoutant l'option --self.
    """


@client_group.command()
@click.option("--nom", help="Le nom du client que vous voudriez voir")
@click.option(
    "--self",
    is_flag=True,
    help="Pour voir les clients que vous representez (équipe commercial)",
)
@click.pass_context
@requires("read a resource")
def show(ctx, nom, self):
    """
    Permet d'afficher les détails d'un client spécifique.
    Les membres de l'équipe commerciale peuvent ajouter l'option --self pour voir les clients qu'ils représentent.'
    """
    click.echo(welcome(ctx.obj["name"], "afficher", "client"))
    # If self is activated, we use the specific functionality of only returning selected clients
    if self:
        if ctx.obj["role"] != "commercial":
            raise click.ClickException(
                "L'option --self sur les clients marche que pour les membres de l'equipe commercial"
            )
        selected_client = client_from_list_or_argument(
            nom, ctx, restrict_for_commercial=True
        )
    else:
        selected_client = client_from_list_or_argument(nom, ctx)

    client = get_specific_client(selected_client)

    display_client({clean_field_names[k]: v for k, v in client.items()})


@client_group.command()
@click.pass_context
@requires("create client")
def add(ctx):
    """
    Permet la création d'un nouveau client.
    """
    user = ctx.obj["name"]
    click.echo(welcome(ctx.obj["name"], "ajouter", "client"))
    fullname = valid_string(100, "Prenom et nom client")
    email = valid_email()
    phone = valid_phone()
    business_name = valid_string(100, "Nom de l'entreprise")
    # Creation date is manually input in case the commercial has developed relationship previously
    created_at = valid_date("Premier contact avec le client (dd/mm/yyyy)")
    # For new creation of clients, updated_at can just be datetime.now so we don't send this arg
    try:
        create_client(user, fullname, email, phone, business_name, created_at)
        click.echo(success("crée", "client"))
    except Exception as e:
        click.echo(f"Unexpected error: {e}")


@client_group.command()
@click.option("--nom", help="Le nom du client que vous voudriez modifier")
@click.pass_context
@requires("update client")
def update(ctx, nom):
    """
    Permet de modifier les coordonnées d'un client.
    Seul le responsable commercial d'un client donné peut effectuer ces modifications.
    """
    click.echo(welcome(ctx.obj["name"], "modifier", "client"))
    # This only shows the clients represented by the specific commercial
    selected_client = client_from_list_or_argument(
        nom, ctx, restrict_for_commercial=True
    )
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
            selectable_users = [v for v in all_commercial if v != ctx.obj["name"]]
            modification = prompt_from_list(
                choose_msg("membre de l'equipe commercial"), selectable_users
            )
        case "fullname":
            modification = valid_string(100, "Le nouveau nom pour le client")
        case "phone":
            modification = valid_phone()
        case "email":
            modification = valid_email()
        case "business_name":
            modification = valid_string(
                100, "Le nouveau nom pour l'entreprise du client"
            )
        case "created_at":
            modification = valid_date("Date du premier contact")
        case "updated_at":
            modification = valid_date("Date du dernier contact")
    try:
        update_client(selected_client, selected_field, modification)
        click.echo(modification_success(selected_field, selected_client))
    except Exception as e:
        click.ClickException(f"Unexpected error: {e}")


@client_group.command()
@click.argument("client_name", required=False)
@click.pass_context
def delete(ctx, client_name):
    # Delete client permission has not been created in db and is not mentioned in cahier des charges
    pass
