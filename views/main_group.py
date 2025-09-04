import rich_click as click

from auth.token import get_stored_jwt_from_file, generate_and_store_jwt, verify_jwt
from auth.exc import AuthError, AuthExpiredError, AuthInvalidError
from db.read import get_user_details
from auth.file_actions import clear_token_file
from messages.messages import logout_success, login_required

from .subgroups.users import user_group
from .subgroups.clients import client_group
from .subgroups.contracts import contract_group
from .subgroups.events import event_group


def login_prompt():
    """
    Demande le nom d'utilisateur et le mot de passe jusqu'à ce que les informations correctes soient fournies.
    """
    while True:
        email = click.prompt(login_required)
        password = click.prompt("Mot de passe")
        try:
            user_details = get_user_details(email, password)
            return generate_and_store_jwt(user_details)
        except Exception as e:
            click.ClickException(e)


@click.group()
@click.pass_context
def cli_main(ctx):
    """
    La fonction principale du click. Tous les sous-groupes sont ajoutés ici.
    La première chose qui se passe est que le script vérifie si le jeton est valide.
    S'il n'y a pas de jeton, une invite de connexion s'affiche.
    """
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
            click.ClickException("JWT expiré.")
        except AuthInvalidError:
            click.ClickException("JWT invalide.")
        except Exception as e:
            click.ClickException(f"Erreur: {e}")


@cli_main.command()
def logout():
    """
    Déconnecte l'utilisateur actuel et supprime son JWT.
    """
    clear_token_file()
    click.echo(logout_success)


cli_main.add_command(user_group)
cli_main.add_command(client_group)
cli_main.add_command(contract_group)
cli_main.add_command(event_group)
