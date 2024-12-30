import click
from gitflux.providers import GitServiceProvider


@click.command('delete-repos')
@click.argument('names', required=False, nargs=-1)
@click.option('--prefix', help='Prefix of repositories to delete.', type=str, default=None, required=False)
@click.pass_context
def delete_repos_command(ctx: click.Context, names: tuple[str], **options: dict):
    """Delete existing repositories."""

    provider: GitServiceProvider = ctx.obj['provider']

    for name in names:
        provider.delete_repo(name)

    if options['prefix'] is None or click.prompt(f'Delete ALL repositories with prefix: {options["prefix"]}, sure?', default='n').lower() == 'n':
        ctx.exit()

    for name in map(lambda repo: repo.full_name, filter(lambda repo: repo.get_prefix() == options['prefix'], provider.get_repos())):
        provider.delete_repo(name)
