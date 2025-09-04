import click

from db.read import (
    get_usernames,
    get_clients,
    get_clients_represented_by_commercial,
    get_all_events,
    get_equipe_usernames,
    get_events_for_support,
)
from messages.messages import list_options, choose_msg


def user_from_list_or_argument(username, equipe):
    """
    User click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the user that should be acted upon.
    """
    equipes = ["gestion", "commercial", "support"]
    all_users = (
        get_usernames() if equipe not in equipes else get_equipe_usernames(equipe)
    )

    if username:
        if username not in all_users:
            click.ClickException(f"Utilisateur '{username}' introuvable.")
            return
        selected_user = username
    else:
        selected_user = prompt_from_list(choose_msg("employé"), all_users)

    return selected_user


def event_from_list_or_argument(event_name, ctx, restrict_for_support=False):
    """
    Event click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the event that should be acted upon.
    """
    all_events = get_all_events()

    if event_name:
        if event_name not in all_events:
            raise click.ClickException(f"Evenement '{event_name}' introuvable.")
        selected_event = event_name
    else:
        if restrict_for_support:
            selectable_events = get_events_for_support()
        else:
            selectable_events = all_events
        selected_event = prompt_from_list(choose_msg("evenement"), selectable_events)

    return selected_event


def client_from_list_or_argument(client_name, ctx, restrict_for_commercial=False):
    """
    User click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the user that should be acted upon.
    """
    all_clients = get_clients()
    if client_name:
        if client_name not in all_clients:
            raise click.ClickException(f"Client '{client_name}' introuvable.")
        selected_client = client_name
    else:
        if restrict_for_commercial and ctx.obj["role"] == "commercial":
            selectable_clients = get_clients_represented_by_commercial(ctx.obj["name"])
        else:
            selectable_clients = all_clients
        selected_client = prompt_from_list(choose_msg("client"), selectable_clients)

    return selected_client


def prompt_from_list(prompt_text, options):
    """
    Display a numbered menu for a list of options and return the selected value.

    :param prompt_text: The question to display
    :param options: A list of valid string options
    :return: The selected option (string)
    """
    # Build numbered map
    numbered_options = {str(i): option for i, option in enumerate(options, start=1)}

    click.echo(prompt_text)
    for number, option in numbered_options.items():
        click.echo(list_options(number, option))
    click.echo()

    choice_num = click.prompt(
        "Quelle option choisissez-vous ?",
        type=click.Choice(numbered_options.keys(), case_sensitive=False),
    )

    return numbered_options[choice_num]


# def optional_prompt(text):
#     value = click.prompt(text, default="", show_default=False)
#     return value or None


def select_from_readable_contracts(contracts, msg):
    """
    This function addresses the fact the contract dictionaries are not useful as readable items.
    It creates readable strings to present to the user and then returns the selected contract from the original list.
    """
    readable_contracts = create_title_strings_from_contracts(contracts)
    selected_readable_contract = prompt_from_list(msg, readable_contracts)
    # Given that I made the list readable, there's an extra step to get the actually selected contract
    selected_contract = contracts[readable_contracts.index(selected_readable_contract)]
    return selected_contract


def create_title_strings_from_contracts(contracts):
    # Helper function for the function above.
    readable_contracts = []
    for contract in contracts:
        readable_string = f"Contrat {contract['id']} d'un montant total de {contract['total_amount']} crée le {contract['created_at']}"
        readable_contracts.append(readable_string)
    return readable_contracts


def get_selected_field(dictionary):
    """
    Takes a dictionary, creates a list of readable key, value pairs, then returns the key name of the
    selected dict item (which is the field that needs to be modified in a db.update request)
    """

    readable_list = [f"{k} ({v})" for k, v in dictionary.items()]

    selected_list_item = prompt_from_list(choose_msg("champ"), readable_list)

    # Obtain just the key from the returned item
    selected_field = selected_list_item.partition(" ")[0]

    return selected_field
