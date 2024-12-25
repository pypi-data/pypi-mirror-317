import click
import time
import json
import os
from multiprocessing import Process, Queue

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.exceptions import (
    NotSupportedProjectException
)
from spb_cli.labels.utils import (
    recursive_glob_label_files,
    file_writer,
)
from spb_label.utils import (
    SearchFilter,
)
from spb_label.exceptions import (
    APIException
)


class UploadLabelService(BaseService):
    MAX_RETRY_COUNT = 3
    def build_image_labels(
        self
    ):
        pass

    def upload_label(
        self,
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

        if project.workapp == "pointclouds-siesta":
            raise NotSupportedProjectException(
                "This project is not supported. Please check the project type."
            )
        else:
            labels = recursive_glob_label_files(directory_path)
            

        if len(labels) == 0:
            click.echo("No label files found in the directory.")
            return
        else:
            click.echo(f"2. Found {len(labels)} label files.")
        
        if not is_forced:
            if not click.confirm(
                f"Uploading {len(labels)} label files to the project. Proceed?",
            ):
                return
        
        labels_queue = Queue()
        success_queue = Queue()
        fail_queue = Queue()

        # Enqueue labels for processor
        for label in labels:
            labels_queue.put(label)
        final_num_process = min(num_process, len(labels))
        for _ in range(final_num_process):
            labels_queue.put(None)

        click.echo(f"3. Start uploading {len(labels)} label files to the project.")

        # Make worker processors
        worker_processors = []
        for i in range(final_num_process):
            worker_process = Process(
                target=self.upload_label_worker,
                args=(i, directory_path, labels_queue, success_queue, fail_queue)
            )
            worker_process.start()
            worker_processors.append(worker_process)
        
        for worker in worker_processors:
            worker.join()
        
        click.echo("4. Complete uploading label files to the project.")

        # Print error logs
        error_labels = []
        while not fail_queue.empty():
            try:
                error_label = fail_queue.get_nowait()
                error_labels.append(error_label)
            except fail_queue.Empty:
                break

        if len(error_labels) > 0:
            log_path = os.path.join(directory_path, 'error.log')
            logs = "\n".join([json.dumps({
                "project_id": str(project.id),
                "project_name": project.name,
                "label_path": item,
            }) for item in error_labels])
            file_writer(
                path=log_path,
                mode="w",
                content=logs
            )
            click.echo(
                f"4. Failed to download {len(error_labels)} labels. Check {log_path} file."
            )

    def upload_label_worker(
        self,
        worker_id: int,
        directory_path: str,
        labels_queue: Queue,
        success_queue: Queue,
        fail_queue: Queue,
    ):
        click.echo(f"  Worker {worker_id} is started.")
        time_window = 0
        while True:
            time.sleep(time_window)
            label_file_path = labels_queue.get()
            if label_file_path is None:
                break
            try:
                real_label_path = os.path.join(directory_path, label_file_path)
                with open(real_label_path, "r") as file:
                    label = json.load(file)
                if (
                    "result" not in label and
                    "data_key" not in label
                ):
                    raise Exception("Invalid label file.")
                filter = SearchFilter()
                filter.data_key_matches = label["data_key"]
                _, handlers, _ = self.client.get_label_ids(
                    filter=filter
                )

                if len(handlers) != 1:
                    raise Exception("Describe label error.")
                else:
                    handler = handlers[0]
                
                handler.data.result = label["result"]
                handler.update_info()
                message = f"[{real_label_path}] to [{handler._project.name}] project"
                click.echo(
                    f"    Uploading... : Success {message}."
                )
                success_queue.put(label_file_path)
            except Exception as e:
                if isinstance(e, APIException):
                    time_window = time_window + 0.2
                fail_queue.put(label_file_path)
                click.echo(
                    f"    Uploading... : Fail to upload {real_label_path}."
                )

            


# superb upload labels -p SDKUploadTest -d ./workspace/download_images -np 4 -y
# superb upload labels -p VideoSDKUploadTest -d ./workspace/download_videos -np 4 -y