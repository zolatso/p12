import click

from auth.token import get_stored_jwt_from_file, generate_and_store_jwt, verify_jwt
from auth.exc import AuthError, AuthExpiredError, AuthInvalidError
from db.crud import get_user_details
from auth.file_actions import clear_token_file
from .users import user_group
from .clients import client_group


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
            ctx.obj["token"] = data
            break
        except AuthExpiredError:
            print("JWT has expired.")
        except AuthInvalidError:
            print("Invalid JWT.")
        except Exception as e:
            print(f"Unexpected error: {e}")

@cli_main.command()
def logout():
    clear_token_file()
    click.echo("Logged out!")

cli_main.add_command(user_group)
cli_main.add_command(client_group)