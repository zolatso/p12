import rich_click as click

from db.read import (
    signed_contracts_by_my_clients, 
    get_all_events, 
    get_events_for_support, 
    get_all_support, 
    get_specific_event
)
from db.create import create_event
from db.update import update_event
from .helper_functions.decorators import requires
from .helper_functions.helpers import (
    prompt_from_list, select_from_readable_contracts, event_from_list_or_argument, get_selected_field
)
from .helper_functions.validators import valid_datetime, valid_string, valid_int

clean_field_names = {
    "name" : "Nom",
    "client_contact" : "Contact pour le client",
    "event_start" : "Debut de l'evenement",
    "event_end" : "Fin de l'evenement",
    "location" : "Lieu",
    "attendees" : "Invités",
    "notes" : "Notes"
}

@click.group()
@click.pass_context
def event_group(ctx):
    """Event commands"""

@event_group.command()
@click.option("––nom", help="Le nom de l'evenement que vous voudriez voir")
@click.pass_context
@requires("read a resource")
def show(ctx, event_name):
    selected_event = event_from_list_or_argument(event_name)
    event = get_specific_event(selected_event)
    for k, v in event.items():
        click.echo(f"{clean_field_names[k]}: {v}")

@event_group.command()
@click.pass_context
@requires("create event")
def add(ctx):
    user = ctx.obj["name"]
    valid_contracts = signed_contracts_by_my_clients(user)

    selected_contract = select_from_readable_contracts(
        valid_contracts, 
        "Veuillez choisir parmi les contrats signés par les clients que vous representez qui n'ont toujours pas d'evenement."
        )

    contract_id = selected_contract["id"]
    event_name = valid_string(100, "Nom de l'evenement")
    event_contact = valid_string(500, "Nom de le contact pour l'evenement")
    event_start = valid_datetime("Debut de l'evenement (dd/mm/yy hh:mm)")
    event_end = valid_datetime("Fin de l'evenement (dd/mm/yy hh:mm)")
    location = valid_string(100, "Lieu")
    attendees = valid_int("Combien d'invités?")
    notes = valid_string(1000, "Notes")

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
        raise click.ClickException(f"Erreur: {e}")
    
@event_group.command()
@click.pass_context
@requires("update event")
def update(ctx):
    # Both gestion and support are able to update events. 
    # However, they have different capacities so we distinguish here.
    role = ctx.obj["role"]
    events = get_all_events() if role == "gestion" else get_events_for_support(ctx.obj["name"])

    selected_event = prompt_from_list(
        "Veuillez choisir l'evenement que vous voudriez modifier",
        events
    )

    # Gestion can only modify the support associated with an event. Separate logic here.
    if role == "gestion":
        equipe_support = get_all_support()
        modification = prompt_from_list(
            "Veuillez choisir le membre de l'equipe support que vous voudriez associer à cet evenement",
            equipe_support
        )
        selected_field_name = "support_id"
    else:
    # Modification for equipe support
    # Logic is slightly different to other updates. THere maybe a redundant db call here.
        event_to_modify = get_specific_event(selected_event)
        selected_field = get_selected_field(event_to_modify)

        match selected_field:
            case "event_start" | "event_end":
                modification = valid_datetime(
                    f"Entrez le nouveau {clean_field_names[selected_field].lower()}"
                )
            case "attendees":
                modification = valid_int("Combien d'invités ?")
            case "name" | "client_contact" | "location" | "notes":
                modification = valid_string(
                    f"Entrez le nouveau {clean_field_names[selected_field].lower()}"
                )
    try:
        update_event(selected_event, selected_field_name, modification)
    except Exception as e:
        click.ClickException(f"Erreur: {e}")  





    




