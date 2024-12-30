import click
from gitflux.providers import GitServiceProvider


@click.command('list-repos')
@click.pass_context
def list_repos_command(ctx: click.Context):
    """List all remote repositories."""

    provider: GitServiceProvider = ctx.obj['provider']

    for repo in provider.get_repos():
        click.echo(repo.full_name)
