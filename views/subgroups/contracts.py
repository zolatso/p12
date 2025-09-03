import rich_click as click

from db.read import get_contracts_for_client
from db.create import create_contract
from db.update import update_contract
from ..helper_functions.decorators import requires
from ..helper_functions.helpers import (
    client_from_list_or_argument, get_clients, prompt_from_list, select_from_readable_contracts,
    get_selected_field
)
from ..helper_functions.validators import valid_int, valid_date

clean_field_names = {
    "total_amount" : "montant total",
    "amount_remaining" : "montant qui reste",
    "created_at" : "date de création",
    "is_signed" : "a été signé"
}


@click.group()
@click.pass_context
def contract_group(ctx):
    """Contract commands"""

@contract_group.command()
@click.option("--nom", help="Le nom du client pour lequel vous voudriez voir les contrats")
@click.pass_context
@requires("read a resource")
def show(ctx, nom):
    selected_client = client_from_list_or_argument(nom, ctx)
    contracts = get_contracts_for_client(selected_client)
    for contract in contracts:
        click.echo("-"*50)
        if "event" in contract: 
            title = f"Le contrat pour l'evenement: {contract["event"]}"
        else:
            title = "Ce contrat n'a toujours pas d'evenement."
        click.echo(title)
        click.echo(f"Valeur du contrat: {contract["total_amount"]}")
        click.echo(f"Montant non payé: {contract["amount_remaining"]}")
        click.echo(f"Commercial associé avec ce contrat: {contract["associated_commercial"]}")
        click.echo(f"Crée le: {contract["created_at"]}")
        if contract["is_signed"]:
            is_signed = "Ce contrat a été signé"
        else:
            is_signed = "Ce contrat n'a toujours pas été signé"
        click.echo(is_signed)

@contract_group.command()
@click.pass_context
@requires("create contract")
def add(ctx):
    user = ctx.obj["name"]
    click.echo(f"Bonjour {user}, vous allez créer un nouveau contrat.")
    clients = get_clients()
    selected_client = prompt_from_list(
            "Veuillez choisir le client pour lequel vous voudriez créer un contrat",
            clients
        )
    
    amount = valid_int("Montant total pour ce contrat")
    amount_remaining = valid_int("Montant qui n'a pas été payé")
    # True argument in the below indicates it is optional
    created_at = valid_date("Date quand le contrat a été crée (laisser vide pour indiquer la date du jour)", optional=True)
    is_signed = click.prompt(
        "Est-ce que le contat a été signé",
        type=click.Choice(["Oui", "Non"], case_sensitive=False)
    )
    try:
        create_contract(
            selected_client,
            amount,
            amount_remaining,
            created_at,
            is_signed
        )
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {e}")

@contract_group.command()
@click.option("--nom", help="Le nom du client pour lequel vous voudriez modifier un contrat")
@click.pass_context
@requires("update contract")
def update(ctx, nom):
    # The additional argument here means that if you are a commercial, you will only be shown
    # the clients that you are a representative of
    selected_client = client_from_list_or_argument(nom, ctx, restrict_for_commercial=True)
    contracts = get_contracts_for_client(selected_client)

    selected_contract = select_from_readable_contracts(
        contracts, 
        "Veuillez choisir le contrat que vous voudriez modifier"
        )

    # Select the fields we want to allow them to modify
    modifiable_fields = {k: v for k, v in selected_contract.items() if k not in ["id", "associated_commercial"]}
    # Present the selection menu
    selected_field = get_selected_field(modifiable_fields)

    # Different behaviors for different fields that require modification
    match selected_field:
        case "created_at":
            modification = valid_date(
                f"Entrez le nouveau {clean_field_names[selected_field]} (dd/mm/yyyy)"
                )
        case "is_signed":
            modification = click.prompt(
                "Est-ce que le contrat a été signé",
                type=click.Choice(["Oui", "Non"], case_sensitive=False)
            )
        case "total_amount" | "amount_remaining":
            modification = valid_int(
                f"Entrez le nouveau {clean_field_names[selected_field]}"
                )
    try:
        update_contract(selected_contract["id"], selected_field, modification)
        click.echo(f"Le {clean_field_names["selected_field"]} de {selected_client} a été modifié.")
    except Exception as e:
        click.ClickException(f"Unexpected error: {e}")

@contract_group.command()
def delete():
    # This requirement is not specified in the cahier des charges
    pass
    



    

    
    
    