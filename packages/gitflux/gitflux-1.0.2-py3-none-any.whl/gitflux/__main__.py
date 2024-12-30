import json
import importlib
from pathlib import Path

import click
from gitflux.commands import command_group


@click.group(commands=command_group)
@click.version_option(message='%(version)s')
@click.option('-p', '--profile-name', help='Name of profile to use.', type=str, required=False, default='default')
@click.pass_context
def cli(ctx: click.Context, profile_name: str):
    """A command-line utility that helps you manage repositories hosted on Git service providers."""

    ctx.ensure_object(dict)

    profile_file = Path().home().joinpath('.config', 'gitflux', 'profiles', profile_name)

    if not profile_file.exists():
        profile_file.parent.mkdir(parents=True, exist_ok=True)

        click.echo(f'Profile "{profile_name}" found, try to generate:')

        profile = {
            'provider': click.prompt('Provider', type=click.Choice(['github', 'gitee']), default='github'),
            'access_token': click.prompt('Access token', hide_input=True)
        }

        profile_file.write_text(json.dumps(profile, ensure_ascii=False, indent=4), encoding='utf-8')
        profile_file.chmod(0o600)
    else:
        profile = json.load(profile_file.open('r', encoding='utf-8'))

    provider_module = importlib.import_module(f'gitflux.providers.{profile["provider"]}')

    ctx.obj['provider'] = provider_module.create_provider(profile['access_token'])


if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    cli()
