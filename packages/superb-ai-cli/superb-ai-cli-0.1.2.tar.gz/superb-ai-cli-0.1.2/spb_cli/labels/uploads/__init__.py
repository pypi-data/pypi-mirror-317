import click

from .upload_data import UploadDataService
from .upload_labels import UploadLabelService
from spb_cli.labels.exceptions import SDKInitiationFailedException


@click.group()
def upload():
    """Upload your data to Superb Platform"""
    pass


@upload.command()
@click.option('-n', '--name', 'name', help='Target dataset name')
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-np', '--num_process', 'num_process', type=int, required=False, default=2, help='Number of processors for executing commands (default=2)')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def dataset(name, project_name, directory_path, num_process, is_forced):
    if not (1 <= num_process and num_process <= 5):
        print("[ERROR] Number of processors should be between 1 and 5.")
        return
    
    if name is None or project_name is None:
        print("[ERROR] You must provide both the dataset name and project name for this command")
        return

    """Upload data to your Superb Platform project"""
    try:
        service = UploadDataService()
        service.upload_data(
            dataset=name,
            project_name=project_name,
            directory_path=directory_path,
            num_process=num_process,
            is_forced=is_forced,
        )
    except SDKInitiationFailedException as e:
        print('No credentials detected. Please use the configure CLI command to register your credentials.')
    except Exception as e:
        raise e


@upload.command()
@click.option('-p', '--project', 'project_name', help='Target project name')
@click.option('-d', '--dir', 'directory_path', default='.', help='Target directory path (default=[./])')
@click.option('-np', '--num_process', 'num_process', type=int, required=False, default=2, help='Number of processors for executing commands (default=2)')
@click.option('-y', '--yes', 'is_forced', required=False, default=False, help='Say YES to all prompts', is_flag=True)
def labels(project_name, directory_path, num_process, is_forced):
    if not (1 <= num_process and num_process <= 5):
        print("[ERROR] Number of processors should be between 1 and 5.")
        return
    
    if project_name is None:
        print("[ERROR] You must provide the project name for this command")
        return

    """Upload label json to your Superb Platform project"""
    try:
        service = UploadLabelService()
        service.upload_label(
            project_name=project_name,
            directory_path=directory_path,
            num_process=num_process,
            is_forced=is_forced,
        )
    except SDKInitiationFailedException as e:
        print('No credentials detected. Please use the configure CLI command to register your credentials.')
    except Exception as e:
        raise e
