import rich_click as click

from db.read import get_contracts_for_client
from db.create import create_contract
from db.update import update_contract
from .helper_functions.decorators import requires
from .helper_functions.helpers import (
    client_from_list_or_argument, get_clients, prompt_from_list, optional_prompt, select_from_readable_contracts
)


@click.group()
@click.pass_context
def contract_group(ctx):
    """User commands"""

@contract_group.command()
@click.argument("client_name", required=False)
@click.pass_context
@requires("read a resource")
def show(ctx, client_name):
    selected_client = client_from_list_or_argument(client_name, ctx)
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
    amount = click.prompt("Montant total pour ce contrat")
    amount_remaining = click.prompt("Montant qui n'a pas été payé")
    created_at = optional_prompt("Date quand le contrat a été crée (laisser vide pour indiquer la date du jour)")
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
@click.argument("client_name", required=False)
@click.pass_context
@requires("update contract")
def update(ctx, client_name):
    # The additional argument here means that if you are a commercial, you will only be shown
    # the clients that you are a representative of
    selected_client = client_from_list_or_argument(client_name, ctx, restrict_for_commercial=True)
    contracts = get_contracts_for_client(selected_client)

    selected_contract = select_from_readable_contracts(
        contracts, 
        "Veuillez choisir le contrat que vous voudriez modifier"
        )

    # Select the fields we want to allow them to modify
    modifiable_fields = [v for k, v in selected_contract.items() if k not in ("id", "associated_commercial")]

    selected_field = prompt_from_list(
        "Veuillez choisir le champ que vous voudriez modifier",
        modifiable_fields
    )
    # There is a bug in this logic if for example the total_amount and amount_outstanding are the same value
    selected_field_name = [field_name for field_name, val in selected_contract.items() if val == selected_field][0]

    # Different behaviors for different fields that require modification
    if selected_field_name == "created_at":
        modification = click.prompt(
            f"Entrez le nouveau {selected_field_name} (dd/mm/yyyy)"
        )
    elif selected_field_name == "is_signed":
        modification = click.prompt(
            "Est-ce que le contat a été signé",
            type=click.Choice(["Oui", "Non"], case_sensitive=False)
        )
    else:
        modification = click.prompt(
            f"Entrez le nouveau {selected_field_name}"
        )
    try:
        update_contract(selected_contract["id"], selected_field_name, modification)
        click.echo(f"Le {selected_field_name} de {selected_client} a été modifié.")
    except Exception as e:
        click.ClickException(f"Unexpected error: {e}")

@contract_group.command()
def delete():
    # This requirement is not specified in the cahier des charges
    pass
    



    

    
    
    