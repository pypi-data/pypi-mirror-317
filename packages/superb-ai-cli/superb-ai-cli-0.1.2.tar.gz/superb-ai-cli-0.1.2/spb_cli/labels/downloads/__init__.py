import click

from .downloads import DownloadService
from spb_cli.labels.exceptions import SDKInitiationFailedException


@click.command()
@click.option(
    '-d', '--dir', 'directory_path',
    default='.',
    help='Target directory path (default=[./])'
)
@click.option(
    '-p', '--project', 'project_name',
    help='Target project name'
)
@click.option(
    '-y', '--yes', 'is_forced',
    required=False,
    default=False,
    help='Say YES to all prompts',
    is_flag=True
)
@click.option(
    '-np', '--num_process', 'num_process',
    type=int,
    required=False,
    default=2,
    help='Number of processors for executing commands (default=2)'
)
def download(
    project_name,
    directory_path,
    is_forced,
    num_process,
):
    """Download all data and labels of your project in Superb Platform """
    if not (1 <= num_process and num_process <= 5):
        print("[ERROR] Number of processors should be between 1 and 5.")
        return

    if project_name is None:
        print("[ERROR] You must provide the project name for this command")
        return

    try:
        service = DownloadService()
        service.download(
            project_name=project_name,
            directory_path=directory_path,
            is_forced=is_forced,
            num_process=num_process,
        )
    except SDKInitiationFailedException as e:
        print('No credentials detected. Please use the configure CLI command to register your credentials.')
    except Exception as e:
        raise e


__all__ = (
    "download",
)
