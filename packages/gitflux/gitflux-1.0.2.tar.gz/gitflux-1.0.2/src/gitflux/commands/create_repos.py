import click
from gitflux.providers import GitServiceProvider


@click.command('create-repos')
@click.argument('names', required=True, nargs=-1)
@click.option('--private', help='Private repository.', is_flag=True, default=True)
@click.pass_context
def create_repos_command(ctx: click.Context, names: tuple[str], **options: dict):
    """Create new repositories."""

    provider: GitServiceProvider = ctx.obj['provider']

    for name in names:
        provider.create_repo(name, private=options['private'])
