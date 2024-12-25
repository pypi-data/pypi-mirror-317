import click

from typing import Optional

from .projects import ProjectService
from spb_cli.labels.exceptions import SDKInitiationFailedException

@click.group()
def describe():
    """Describe your resources in Superb Platform"""
    pass


@describe.command()
@click.option(
    "-s",
    "--show",
    "show_options",
    default="default",
    help="Show which information about projects for the given option : (default | reviews)",
)
@click.option(
    "-d",
    "--data",
    "data_type",
    default="all",
    help="Select the project data type to show : (all | image | video | pointcloud)"
)
@click.option(
    "-n",
    "--name",
    "project_name",
    default=None,
    help="The substring to search for within the project name"
)
def projects(
    show_options: str,
    data_type: str,
    project_name: Optional[str],
):
    try:
        service = ProjectService()
        service.show_projects(
            show_options, data_type, project_name,
        )
    except SDKInitiationFailedException as e:
        print('No credentials detected. Please use the configure CLI command to register your credentials.')
    except Exception as e:
        raise e


__all__ = (
    'describe',
)
