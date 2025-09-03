import functools
import click

def framed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        click.echo()  # blank line
        click.echo("-" * 80)
        result = func(*args, **kwargs)
        click.echo(result)
        click.echo("-" * 80)
        click.echo()  # blank line
    return wrapper