import click

from db.read import get_usernames, get_clients

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

def client_from_list_or_argument(client_name):
    """
    User click views take an optional username argument.
    This function handles the possible cases where such an argument is supplied and where it is not,
    and returns the user that should be acted upon.
    """
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