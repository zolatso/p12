import functools
import click
import random
from .ansi_escape_codes import * 

def framed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        color = random.choice(color_list)
        click.echo()  # blank line
        click.echo(f"{color}{BOLD}-{RESET}" * 80)
        result = func(*args, **kwargs)
        click.echo(result)
        click.echo(f"{color}{BOLD}-{RESET}" * 80)
        click.echo()  # blank line
    return wrapper