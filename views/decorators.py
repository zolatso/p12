import click
from functools import wraps

from .errors import perm_denied

def requires(permission):
    """Decorator to enforce a required permission on a Click command."""
    def decorator(f):
        @wraps(f)
        @click.pass_context
        def wrapper(ctx, *args, **kwargs):
            permissions = ctx.obj["permissions"]
            role = ctx.obj["role"]
            if permission not in permissions:
                raise click.ClickException(perm_denied(role))
            return f(*args, **kwargs)
        return wrapper
    return decorator

