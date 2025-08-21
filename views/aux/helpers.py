import click

from db.read import get_usernames, get_clients, get_clients_represented_by_commercial

def user_from_list_or_argument(username):
    """
    User click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the user that should be acted upon.
    """
    all_users = get_usernames()

    if username:
        if username not in all_users:
            click.echo(f"Utilisateur '{username}' introuvable.")
            return
        selected_user = username
    else:
        selected_user = prompt_from_list(
            "Veuillez choisir un utilisateur dans la liste de tous les utilisateurs (entrez le numéro)",
            all_users
        )
    
    return selected_user

def client_from_list_or_argument(client_name, ctx, restrict_for_commercial=False):
    """
    User click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the user that should be acted upon.
    """
    if restrict_for_commercial and ctx.obj["role"] == "commercial":
        all_clients = get_clients_represented_by_commercial(ctx["user"])
    else:
        all_clients = get_clients()

    if client_name:
        if client_name not in all_clients:
            click.echo(f"Client '{client_name}' introuvable.")
            return
        selected_client = client_name
    else:
        selected_client = prompt_from_list(
            "Veuillez choisir un client dans la liste de tous les clients (entrez le numéro)",
            all_clients
        )
    
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
        click.echo(f"{number}. {option}")

    choice_num = click.prompt(
        "Enter the number of your choice",
        type=click.Choice(numbered_options.keys(), case_sensitive=False)
    )

    return numbered_options[choice_num]

def optional_prompt(text):
    value = click.prompt(text, default="", show_default=False)
    return value or None

def select_from_readable_contracts(contracts, msg):
    """
    This function addresses the fact the contract dictionaries are not useful as readable items.
    It creates readable strings to present to the user and then returns the selected contract from the original list.
    """
    readable_contracts = create_title_strings_from_contracts(contracts)
    selected_readable_contract = prompt_from_list(
        msg,
        readable_contracts
    )
    # Given that I made the list readable, there's an extra step to get the actually selected contract
    selected_contract = contracts[readable_contracts.index(selected_readable_contract)]
    return selected_contract

def create_title_strings_from_contracts(contracts): 
    # Helper function for the function above.
    readable_contracts = []
    for contract in contracts:
        readable_string = f"Contrat {contract["id"]} d'un montant total de {contract["total_amount"]} crée le {contract["created_at"]}"
        readable_contracts.append(readable_string)
    return readable_contracts