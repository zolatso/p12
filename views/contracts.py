import click

from db.read import get_contracts_for_client
from db.create import create_contract
from .aux.decorators import requires
from .aux.helpers import client_from_list_or_argument, get_clients, prompt_from_list, optional_prompt


@click.group()
@click.pass_context
def contract_group(ctx):
    """User commands"""

@contract_group.command()
@click.argument("client_name", required=False)
@click.pass_context
@requires("read a resource")
def show(ctx, client_name):
    selected_client = client_from_list_or_argument(client_name)
    contracts = get_contracts_for_client(selected_client)
    for contract in contracts:
        click.echo("-"*50)
        if contract["event"]: 
            title = f"Le contrat pour l'evenement: {contract["event"]}"
        else:
            title = "Ce contrat n'a toujours pas un evenement."
        click.echo(title)
        click.echo(f"Valeur du contrat: {contract["total_amount"]}")
        click.echo(f"Montant non payé: {contract["amount_remaining"]}")
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
    selected_client = client_from_list_or_argument(client_name)
    client = get_contracts_for_client(selected_client)

    # Extra permission required here: All members of equipe gestion can modify a contract,
    # but among the commercial team, only the commercial associated with the contract can modify
    user = ctx.obj["name"]
    associated_commercial = client["user"]
    if not user == associated_commercial:
        raise click.ClickException(
            f"""Vous n'êtes pas le commercial associé à ce client, vous ne pouvez donc pas modifier ses coordonnées.
            Veuillez contacter {associated_commercial}, qui est son représentant."""
            )
    
    # Here we remove contracts from the fields that can be modified as this doesn't seem like a good idea.
    modifiable_fields = [v for k, v in client.items() if k != "contracts"]

    selected_field = prompt_from_list(
        "Veuillez choisir le champ que vous voudriez modifier",
        modifiable_fields
    )
    
    selected_field_name = [field_name for field_name, val in client.items() if val == selected_field][0]

    # If user wants to modify the commercial associated with the client, different behavior is required.
    if selected_field_name == "user":
        all_commercial = get_commercial_usernames()
        # Get rid of the current user who logically must be the commercial currently associated with this client,
        # as they passed the permission check earlier
        selectable_users = [v for v in all_commercial if v != user]
        modification = prompt_from_list(
            "Veuillez choisir le commercial que vous voudriez associé à ce client",
            selectable_users
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

    
    
    