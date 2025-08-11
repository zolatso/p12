import click
from exc.exc import AuthError
from db.crud import get_user
from .users import user_group

@click.group()
@click.pass_context
def cli_main(ctx):
    # auth logic here, ctx.obj setup etc.
    ctx.ensure_object(dict)
    ctx.obj["token"] = "some token info or object"

cli_main.add_command(user_group)