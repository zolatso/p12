import click
from exc.exc import AuthError
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
        click.echo(user.clients)
    except AuthError:
        click.echo("Sorry, the user or password is incorrect.")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")