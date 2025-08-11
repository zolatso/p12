import click
from .users import user_group
from auth.token import get_stored_jwt_from_file, generate_and_store_jwt, verify_jwt
from db.crud import get_user_details

def login_prompt():
    email = click.prompt("You are not logged in. Enter email")
    password = click.prompt("Enter password")
    user_details = get_user_details(email, password)
    return generate_and_store_jwt(user_details)

@click.group()
@click.pass_context
def cli_main(ctx):
    token = get_stored_jwt_from_file()
    if not token:
        token = login_prompt()
    data = verify_jwt(token)
    ctx.ensure_object(dict)
    ctx.obj["token"] = data



cli_main.add_command(user_group)