import sys
import os
import glob
import time
import random
import requests
import imghdr
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util import Retry
from pathlib import Path


def print_table(
    data
):
    longest_cols = [
        (max([len(str(row[i])) for row in data]) + 3)
        for i in range(len(data[0]))
    ]
    row_format = "".join(
        [
            "{:<" + str(longest_col) + "}"
            for longest_col in longest_cols
        ]
    )
    for row in data:
        print(row_format.format(*row))


def divide_list(lst, n):
    # Calculate the length of each part
    part_length = len(lst) // n
    remainder = len(lst) % n

    # Initialize start index
    start = 0

    # Divide the list into n parts using slicing
    parts = []
    for i in range(n):
        end = start + part_length + (1 if i < remainder else 0)
        parts.append(lst[start:end])
        start = end

    return parts


def erase_line():
    sys.stdout.write("\033[K")  # ANSI 이스케이프 시퀀스를 사용하여 현재 줄을 지웁니다.
    sys.stdout.flush()  # 버퍼를 비워서 변경 사항을 즉시 터미널에 반영합니다.


def random_sleep(start: int, end: int):
    sleep_time = random.uniform(start, end)
    time.sleep(sleep_time)


def requests_retry_session(
    retries=5,
    backoff_factor=0.5,
    status_forcelist=(500, 502, 504),
    session=None,
    allowed_methods=[
        'GET',
        'POST',
        'PUT',
        'DELETE',
        'OPTIONS',
        'HEAD',
        'PATCH',
        'TRACE',
        'CONNECT'
    ]
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=frozenset(allowed_methods),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def file_writer(
    path: str, mode: str, content: any
):
    path = Path(path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    path.open(mode).write(content)


def recursive_glob_image_files(input_path):
    support_img_format = ['png', 'jpg', 'bmp', 'jpeg']
    imgs_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, "**/*"), recursive=True))
    for file_path in select_image_files(files_path):
        if '@' not in file_path and not os.path.isdir(file_path):
            img_format = imghdr.what(file_path)
            if img_format in support_img_format:
                key = extract_file_key(input_path, file_path)
                imgs_path[key] = file_path

    return imgs_path


def select_image_files(file_list):
    image_file_list = []
    support_img_format = ('.png', '.jpg', '.bmp', '.jpeg')
    for file_name in file_list:
        if file_name.lower().endswith(support_img_format):
            image_file_list.append(file_name)
    return image_file_list


def recursive_glob_video_paths(input_path):
    support_img_format = ['png', 'jpg', 'bmp', 'jpeg']
    video_paths = {}
    for dirpath, dirnames, files in os.walk(input_path):
        if len(files) != 0 and dirpath != input_path:
            image_file_list = select_image_files(files)
            if len(image_file_list) != 0:
                key = extract_file_key(input_path, dirpath)
                video_paths[key] = {'path': dirpath, 'file_names': image_file_list}
    return video_paths


def recursive_glob_label_files(input_path):
    support_label_format = ['.json']
    labels_path = {}
    files_path = sorted(glob.glob(os.path.join(input_path, "**/*"), recursive=True))

    for file_path in files_path:
        if '@' not in file_path and not os.path.isdir(file_path):
            file_format = os.path.splitext(file_path)[1]
            if file_format in support_label_format:
                key = extract_file_key(input_path, file_path)
                labels_path[key] = file_path
    return labels_path


def extract_file_key(input_folder_path, file_path):
    key = os.path.abspath(file_path).replace(os.path.abspath(input_folder_path), "")
    key = "/".join(key.split(os.sep)[1:])
    return key


def extract_error_log_from_handler(handler, error):
    if handler is not None:
        return json.dumps({
            "project_id": str(handler._project.id),
            "project_name": handler._project.name,
            "label_id": str(handler.get_id()),
            "dataset_name": handler.get_dataset_name(),
            "key": handler.get_key(),
            "error": str(error),
        })
    else:
        return json.dumps({
            "error": str(error),
        })
