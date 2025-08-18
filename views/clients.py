import click

from db.crud import create_client

@click.group()
@click.pass_context
def client_group(ctx):
    """User commands"""

@client_group.command()
@click.pass_context
def add(ctx):
    # Check permissions
    permissions = ctx.obj["permissions"]
    if "create client" in permissions:
        user = ctx.obj["name"]
        click.echo(f"Bienvenu, {user}. Vous allez ajouter un nouveau client.")
        fullname = click.prompt("Nom et prenom du client")
        email = click.prompt("Email")
        phone = click.prompt("Numero de telephone")
        business_name = click.prompt("Nom de l'entreprise")
        # Creation date is manually input in case the commercial has developed relationship previously
        created_at = click.prompt("Premier contact avec le client (dd/mm/yyyy)")
        # For new creation of clients, updated_at can just be datetime.now so we don't send this arg
        try:
            create_client(
                user,
                fullname,
                email,
                phone,
                business_name,
                created_at
            )
        except Exception as e:
            click.echo(f"Unexpected error: {e}")
    else:
        click.echo("Vous n'avez pas le droit de faire cet action.")







    