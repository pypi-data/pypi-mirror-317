import os
import json
import click
from multiprocessing import Pool
from functools import partial
from pathlib import Path

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.exceptions import (
    NotSupportedProjectException,
    DescribeLabelException,
)
from spb_cli.labels.utils import (
    divide_list,
    erase_line,
    random_sleep,
    requests_retry_session,
    file_writer,
    extract_error_log_from_handler,
)


class DownloadService(BaseService):
    def download(
        self,
        project_name: str,
        directory_path: str,
        is_forced: bool,
        num_process: int,
    ):
        self.client.set_project(
            name=project_name,
        )
        
        try:
            label_count = self.client.get_num_labels()
        except Exception as e:
            raise DescribeLabelException(
                f"Cannot describe labels count. {str(e)}"
            )

        try:
            file_writer(
                path=os.path.join(directory_path, 'project.json'),
                mode="w",
                content=json.dumps(
                    self.client.project.label_interface,
                    indent=4
                )
            )
            click.echo(
                "1. Complete downloading project label interface."
            )
        except Exception as e:
            click.echo(
                "1. Failed downloading project label interface."
            )

        if label_count == 0:
            click.echo(
                "2. Label count is 0. download success."
            )
            return
        else:
            if not is_forced:
                if not click.confirm(
                    f"Downloading {label_count} labels and data from project to [{directory_path}]. Proceed?"
                ):
                    return

            if (
                self.client.project.workapp == 'image-siesta'
            ):
                const = {
                    "processing_label_count": 100,
                    "download_method": self.download_image_label
                }
            elif (
                self.client.project.workapp == 'video-siesta'
            ):
                const = {
                    "processing_label_count": num_process,
                    "download_method": self.download_video_label
                }
            else:
                raise NotSupportedProjectException(
                    f"{self.client.project.workapp} is not supported."
                )

            click.echo(
                f"2. Start downloading {label_count} labels."
            )
            original_num_process = num_process
            cursor = None
            failed_handlers = []
            success_count = 0
            fail_count = 0
            while True:
                num_process = original_num_process
                try:
                    _, handlers, cursor = self.client.get_label_ids(
                        cursor=cursor,
                        page_size=const["processing_label_count"],
                    )
                except:
                    click.echo(
                        "[WARNING] Collecting labels temporary error has occurred. Retry from fault."
                    )
                    random_sleep(1, 5)
                    continue

                if len(handlers) < num_process:
                    # Fix amount of sub process
                    num_process = len(handlers)

                divided_handlers = divide_list(
                    handlers,
                    num_process,
                )
                with Pool(
                    processes=num_process
                ) as p:
                    results = p.map(
                        const["download_method"],
                        zip(
                            range(num_process),
                            [directory_path]*num_process,
                            divided_handlers,
                        ),
                    )
                for result in results:
                    success_count += len(result["success"])
                    fail_count += len(result["failed"])
                    failed_handlers += result["failed"]
                
                click.echo(
                    f"    Downloading... : {success_count}/{label_count} labels has been downloaded. {fail_count} failed."
                )

                if cursor is None:
                    break
            
            click.echo(
                f"3. Complete downloading all labels and data."
            )
            # Print error logs
            if len(failed_handlers) > 0:
                log_path = os.path.join(directory_path, 'error.log')
                logs = "\n".join([extract_error_log_from_handler(
                    handler=item.get("handler", None),
                    error=item.get("error", None),
                ) for item in failed_handlers])
                file_writer(
                    path=log_path,
                    mode="w",
                    content=logs
                )
                click.echo(
                    f"4. Failed to download {len(failed_handlers)} labels. Check {log_path}file."
                )

    def _process_data_builder(
        self, handlers
    ):
        data = []
        for handler in handlers:
            data.append({
                "retry_count": 0,
                "handler": handler,
                "error": None
            })
        return data

    def _download_path_builder(
        self, directory_path, handler
    ):
        path = os.path.join(
            handler.get_dataset_name(),
            handler.get_key()[1:],
        ) if handler.get_key().startswith('/') else os.path.join(
            handler.get_dataset_name(),
            handler.get_key(),
        )
        path = os.path.join(
            directory_path, path
        )
        return path

    def download_image_label(
        self,
        params
    ):
        MAX_RETRY_COUNT = 3
        [_, directory_path, handlers] = params

        success_list = []
        failed_list = []
        data = self._process_data_builder(handlers)
        for item in data:
            try:
                handler = item["handler"]
                path = self._download_path_builder(
                    directory_path=directory_path,
                    handler=handler,
                )
                file_writer(
                    path=f'{path}.json',
                    mode="w",
                    content=json.dumps(
                        handler.data.to_json(),
                        indent=4
                    )
                )
                image_root_path = os.path.join(
                    directory_path, handler.get_dataset_name()
                )
                # Download image
                handler.download_image(
                    download_to=Path(image_root_path)
                )
            except Exception as e:
                item["retry_count"] += 1
                if item["retry_count"] == MAX_RETRY_COUNT:
                    item["error"] = str(e)
                    failed_list.append(item)
                else:
                    data.append(item)
                continue
            success_list.append(item)  # Add item to success list
        return {
            "success": success_list,
            "failed": failed_list,
        }

    def download_video_label(
        self,
        params,
    ):
        MAX_RETRY_COUNT = 3
        [_, directory_path, handlers] = params

        success_list = []
        failed_list = []
        data = self._process_data_builder(handlers)
        for item in data:
            try:
                handler = item["handler"]
                path = self._download_path_builder(
                    directory_path=directory_path,
                    handler=handler,
                )
                file_writer(
                    path=f"{path}.json",
                    mode="w",
                    content=json.dumps(
                        handler.data.to_json(),
                        indent=4
                    )
                )
                video_root_path = os.path.join(
                    directory_path, handler.get_dataset_name(), handler.get_key()
                )
                handler.download_video(
                    download_to=Path(video_root_path),
                )
            except Exception as e:
                item["retry_count"] += 1
                if item["retry_count"] == MAX_RETRY_COUNT:
                    item["error"] = str(e)
                    failed_list.append(item)
                else:
                    data.append(item)
                continue
            success_list.append(item)  # Add item to success list
        return {
            "success": success_list,
            "failed": failed_list,
        }


# superb download -d ./workspace/download_images -p SDKUploadTest -y -np 6
# superb download -d ./workspace/download_videos -p VideoSDKUploadTest -y -np 4