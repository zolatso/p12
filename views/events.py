import rich_click as click

from db.read import signed_contracts_by_my_clients
from db.create import create_event
from .aux.decorators import requires
from .aux.helpers import prompt_from_list, select_from_readable_contracts

@click.group()
@click.pass_context
def event_group(ctx):
    """Event commands"""

@event_group.command()
@click.pass_context
@requires("create event")
def add(ctx):
    user = ctx.obj["user"]
    valid_contracts = signed_contracts_by_my_clients(user)

    selected_contract = select_from_readable_contracts(
        valid_contracts, 
        "Veuillez choisir parmi les contrats signés par les clients que vous representez qui n'ont toujours pas d'evenement."
        )

    contract_id = selected_contract["id"]
    event_name = click.prompt("Nom de l'evenement")
    event_contact = click.prompt("Nom de le contact pour l'evenement")
    # Check format here
    event_start = click.prompt("Debut de l'evenement")
    event_end = click.prompt("Fin de l'evenement")
    location = click.prompt("Lieu")
    attendees = click.prompt("Combien d'invités?")
    notes = click.prompt("Notes")

    try:
        create_event(
            contract_id,
            event_name,
            event_contact,
            event_start,
            event_end,
            location,
            attendees,
            notes
        )
    except Exception as e:
        raise click.ClickException(f"Unexpected error: {e}")



