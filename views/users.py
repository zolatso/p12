import click

@click.group()
@click.pass_context
def user_group(ctx):
    """User commands"""

@user_group.command()
@click.argument("name")
@click.pass_context
def add(ctx, name):
    pass

@user_group.command()
@click.argument("name")
@click.pass_context
def delete(ctx, name):
    pass