import click
import time
import os
import json
from multiprocessing import Process, Queue

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.exceptions import (
    NotSupportedProjectException
)
from spb_cli.labels.utils import (
    recursive_glob_image_files,
    recursive_glob_video_paths,
    divide_list,
    file_writer,
)


class UploadDataService(BaseService):
    def build_image_assets(
            self,
            dataset: str,
            directory_path: str,
    ):
        images_path = recursive_glob_image_files(directory_path)
        return [{
            "file": file_path,
            "data_key": key,
            "dataset": dataset,
        } for key, file_path in images_path.items()]

    def build_video_assets(
            self,
            dataset: str,
            directory_path: str,
    ):
        video_paths = recursive_glob_video_paths(directory_path)
        return [{
            "file": file["path"],
            "data_key": key,
            "dataset": dataset,
        } for key, file in video_paths.items()]

    def upload_data(
        self,
        dataset: str,
        project_name: str,
        directory_path: str = ".",
        num_process: int = 2,
        is_forced: bool = False,
    ):
        self.client.set_project(
            name=project_name,
        )
        project = self.client.project
        click.echo(
            "1. Complete describing project."
        )

        if project.workapp == "image-siesta":
            assets = self.build_image_assets(
                directory_path=directory_path,
                dataset=dataset,
            )
            worker = self.upload_image_worker
        elif project.workapp == "video-siesta":
            assets = self.build_video_assets(
                directory_path=directory_path,
                dataset=dataset,
            )
            worker = self.upload_video_worker
        else:
            raise NotSupportedProjectException("Only image and video projects are supported for now.")
        
        if len(assets) == 0:
            click.echo("No data found.")
            return
        else:
            click.echo(f"2. Found {len(assets)} data.")
        
        if not is_forced:
            if not click.confirm(
                f"Uploading {len(assets)} data to project {project.name}. Proceed?"
            ):
                return
        
        asset_queue = Queue()
        success_queue = Queue()
        fail_queue = Queue()

        # Enqueue messages for process
        for asset in assets:
            asset_queue.put(asset)
        finall_num_process = min(num_process, len(assets))
        for _ in range(finall_num_process):
            asset_queue.put(None)
        
        click.echo("3. Start uploading data.")

        # Make worker processors
        worker_processors = []        
        for i in range(finall_num_process):
            processor_process = Process(target=worker, args=(
                i,
                asset_queue,
                success_queue,
                fail_queue,
            ))
            processor_process.start()
            worker_processors.append(processor_process)
        
        for worker in worker_processors:
            worker.join()

        click.echo(
            f"4. Complete uploading data."
        )
        # Print error logs
        error_assets = []
        while not fail_queue.empty():
            try:
                error_asset = fail_queue.get_nowait()
                error_assets.append(error_asset)
            except fail_queue.Empty:
                break

        if len(error_assets) > 0:
            log_path = os.path.join(directory_path, 'error.log')
            logs = "\n".join([json.dumps(item) for item in error_assets])
            file_writer(
                path=log_path,
                mode="w",
                content=logs
            )
            click.echo(
                f"4. Failed to download {len(error_assets)} labels. Check {log_path} file."
            )
    
    def upload_image_worker(
            self,
            processor_index,
            asset_queue,
            success_queue,
            fail_queue,
    ):
        click.echo(f"  Worker {processor_index} is started.")
        time.sleep(1)
        while True:
            asset = asset_queue.get()
            if asset is None:
                break
            is_success = True
            try:
                result = self.client.upload_image(
                    path=asset["file"],
                    key=asset["data_key"],
                    dataset_name=asset["dataset"],
                )
                if result:
                    success_queue.put(asset)
                else:
                    raise Exception("Failed to upload.")
            except Exception as e:
                is_success = False
                fail_queue.put(asset)
            message = f"[{asset['file']}] to [{asset['dataset']}] dataset"
            click.echo(
                f"    Uploading... : {'Success' if is_success else 'Fail'} {message}."
            )
    
    def upload_video_worker(
            self,
            processor_index,
            asset_queue,
            success_queue,
            fail_queue,
    ):
        click.echo(f"  Worker {processor_index} is started.")
        time.sleep(1)
        while True:
            asset = asset_queue.get()
            if asset is None:
                break
            is_success = True
            try:
                result = self.client.upload_video(
                    path=asset["file"],
                    key=asset["data_key"],
                    dataset_name=asset["dataset"],
                )
                if result:
                    success_queue.put(asset)
                else:
                    raise Exception("Failed to upload.")
            except:
                is_success = False
                fail_queue.put(asset)

            message = f"[{asset['file']}] to [{asset['dataset']}] dataset"
            click.echo(
                f"    Uploading... : {'Success' if is_success else 'Fail'} {message}."
            )


# superb upload dataset -p SDKUploadTest -d ./workspace/images -np 4 -y -n 1
# superb upload dataset -p VideoSDKUploadTest -d ./workspace/videos -np 4 -y -n 2