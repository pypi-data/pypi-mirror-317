import click


@click.group()
def create():
    """Create your data to Superb Platform"""
    pass


@create.command()
@click.option('-p', '--project', 'project_name', help='Created project name')
@click.option('-c', '--project_config_path', 'project_config_path', help='Project config path')
def project():
    pass
