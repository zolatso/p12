import click
from exc import UserDoesNotExistError, InvalidPasswordError
from db.crud import get_user 

@click.command()
@click.argument('email', required=False)
def authenticate(email):
    """
    CLI tool for user login.
    """
    if not email:
        email = click.prompt("Enter your email")

    password = click.prompt("Enter your password", hide_input=True)

    try:
        user = get_user(email, password)
        click.echo(f"Successfully logged in user: {user.name}.")
    except UserDoesNotExistError:
        click.echo("Sorry, that user doesn't exist.")
    except InvalidPasswordError:
        click.echo("Incorrect password.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")