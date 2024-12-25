import io
import json
import os

import click
import configparser

from spb_cli.labels import (
    describe,
    download,
    upload,
)


def load_config():
    current_dir = os.path.dirname(__file__)
    config_path = os.path.join(current_dir, 'config.json')
    with io.open(config_path, 'r', encoding='utf-8') as fid:
        return json.load(fid)


CONFIGS = load_config()


@click.group()
@click.version_option(
    version=CONFIGS["CLI_VERSION"],
    message="Superb Platform CLI. version %(version)s",
)
def cli():
    pass


@cli.command()
def version():
    click.echo(CONFIGS["CLI_VERSION"])


@cli.command()
@click.option('-n', '--team_name', required=False, help="Your team name")
@click.option('-k', '--access_key', required=False, help="Your access key")
@click.option('-l', '--list', 'list_flag', is_flag=True, help="Displays all your configurations")
def configure(team_name, access_key, list_flag):
    """Config your CREDENTIALS(Profile Name, Access Key)"""
    profile_name = 'default'

    if list_flag:
        credential_path = os.path.join(
            os.path.expanduser('~'), '.spb', 'config'
        )
        try:
            with open(credential_path, 'r') as f:
                print(f.read())
        except:
            print(
                "Credential is not configured. Plz, Config your credential first."
            )
        return

    if team_name is None:
        team_name = click.prompt('Superb Platform Team Name', type=str)
    if access_key is None:
        access_key = click.prompt('Access Key', type=str)

    credential_path = os.path.join(os.path.expanduser('~'), '.spb', 'config')
    credential_dir = (os.sep).join(credential_path.split(os.sep)[:-1])

    os.makedirs(credential_dir, exist_ok=True)

    config_parser = configparser.ConfigParser()
    config_parser.read(credential_path)
    config_parser[profile_name] = {
        'team_name': team_name,
        'access_key': access_key,
    }

    with open(credential_path, 'w') as f:
        config_parser.write(f)

    print(
        f"Profile [{profile_name}] is configured with team name '{team_name}'."
    )


cli.add_command(describe)
cli.add_command(download)
cli.add_command(upload)


if __name__ == "__main__":
    cli()
