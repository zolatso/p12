import rich_click as click

from auth.token import get_stored_jwt_from_file, generate_and_store_jwt, verify_jwt
from auth.exc import AuthError, AuthExpiredError, AuthInvalidError
from db.read import get_user_details
from auth.file_actions import clear_token_file
from .subgroups.helper_functions.ansi_escape_codes import *
from .subgroups.users import user_group
from .subgroups.clients import client_group
from .subgroups.contracts import contract_group
from .subgroups.events import event_group


def login_prompt():
    while True:
        email = click.prompt("You are not logged in. Enter email")
        password = click.prompt("Enter password")
        try:
            user_details = get_user_details(email, password)
            return generate_and_store_jwt(user_details)
        except AuthError as e:
            print(e)
            print("Please try again.\n")

@click.group()
@click.pass_context
def cli_main(ctx):
    while True:
        token = get_stored_jwt_from_file()
        if not token:
            token = login_prompt()
        try:    
            data = verify_jwt(token)
            ctx.ensure_object(dict)
            ctx.obj = data
            break
        except AuthExpiredError:
            click.ClickException("JWT has expired.")
        except AuthInvalidError:
            click.ClickException("Invalid JWT.")
        except Exception as e:
            click.ClickException(f"Unexpected error: {e}")

@cli_main.command()
def logout():
    """
    Logouts out the current user and removes their JWT.
    """
    clear_token_file()
    click.echo(f"{BOLD}{MAGENTA}Vous vous êtes déconnecté avec succès.{RESET}")

cli_main.add_command(user_group)
cli_main.add_command(client_group)
cli_main.add_command(contract_group)
cli_main.add_command(event_group)