# `superb-ai-cli`

[![Version](https://img.shields.io/pypi/v/superb-ai-cli)](https://pypi.org/project/superb-ai-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview

`superb-ai-cli` is the command line interface for interacting with [Superb Platform](https://superb-ai.com/).

## Installation

You don't need this source code unless you want to modify the package. If you just want to use the package, just run:

```shell
$ pip install --upgrade superb-ai-cli
$ superb --version

Superb Platform CLI. version 0.1.x
```

Once installed, you can type superb command in the terminal to access the command line interface.

### Requirements

Python 3.7+

### Authentication

You need an Access Key for authentication. The Access Key can be generated on the 🎉 Superb AI Platform web (Platform > Settings > Access).

You can then configure your profile by entering your Platform Team Name and the generated Access Key.

🚨 Platform Team Name refers to the organization name that your personal account belongs to:

<img src="./assets/login.png" width="400">

```bash
$ superb configure

Superb Platform Team Name: foo
Access Key: bar
```

Once configured, you can check the currently configured profile by using the `--list` option.

```bash
$ superb configure --list

[default]
access_key = foo
team_name = bar
```

## Resource Description

### Projects

You can list all projects that belong to the currently configured profile by using the following command:

```bash
$ superb describe projects

NAME                               DATA_TYPE   LABELS   IN_PROGRESS    SUBMITTED    SKIPPED   
my-project                         image       20       19 (95 %)      1 (5 %)      0 (0 %)   
...
Press any button to continue to the next page (1/10). Otherwise press ‘Q’ to quit.

$ superb describe project --show reviews
INR   IN PROGRESS : Rejected        
INN   IN PROGRESS : Not Submitted   
SUA   SUBMITTED : Approved          
SUP   SUBMITTED : Pending Review    
SKA   SKIPPED : Approved            
SKP   SKIPPED : Pending Review

NAME                               DATA_TYPE   LABELS   INR   INN    SUA   SUP   SKA   SKP   
my-project                         image       20       0     19     0     1     0     0     
...
Press any button to continue to the next page (1/10). Otherwise press ‘Q’ to quit.
```

## Uploading Dataset & Labels

You can upload data and create labels for your project with this command line interface.

Move to the dataset directory that has image files (with extension of `.jpg`, `.png`, `.gif`) and upload images in the directory by using the following CLI command:

```bash
$ superb upload dataset --name <target_dataset_name> --project <target_project_name> --dir <target_directory>
$ superb upload dataset -n <target_dataset_name> -p <target_project_name> -d <target_directory>
[INFO] Set project success: <target_project_name>
1. Complete describing project.
2. Found 20 data.
Uploading 20 data to project <target_project_name>. Proceed? [y/N] y
3. Start uploading data.
  Worker 0 is started.
  Worker 1 is started.
    Uploading... : Success [<target_directory>/xxx and xxx1.jpg] to [<target_dataset_name>] dataset.
    Uploading... : Success [<target_directory>/xxx and xxx2.jpg] to [<target_dataset_name>] dataset.
4. Complete uploading data.
```

If you wish to upload the **label** files along with the dataset

```shell
$ superb upload labels --project <target_project_name> --dir <target_directory>
$ superb upload labels -p <target_project_name> -d <target_directory>
[INFO] Set project success: <target_project_name>
1. Complete describing project.
2. Found 20 label files.
Uploading 20 label files to the project. Proceed? [y/N]: y
3. Start uploading 20 label files to the project.
  Worker 0 is started.
  Worker 1 is started.
    Uploading... : Success [<target_directory>/xxx/xxx1.jpg.json] to [<target_project_name>] project.
    Uploading... : Success [<target_directory>/xxx/xxx2.jpg.json] to [<target_project_name>] project.
4. Complete uploading label files to the project.
```

To learn how to create a **label** JSON file according to the Superb AI format, please refer to the **Annotation JSON File Structure** section in the linked [Superb AI Platform Manual](https://docs.superb-ai.com/reference/uploading-raw-data-and-labels#uploading-label-files-only).

## Downloading Data & Labels

You can download images and labels for a project by using the following command:

```bash
$ superb download --dir <target_directory> --project <target_project_name>
$ superb download -d <target_directory> -p <target_project_name>
[INFO] Set project success: <target_project_name>
1. Complete downloading project label interface.
Downloading 20 labels and data from project to [<target_project_name>]. Proceed? [y/N]: y
2. Start downloading 20 labels.
[INFO] Downloaded to <target_directory>/xxxxx
[INFO] Downloaded to <target_directory>/xxxxx
[INFO] Downloaded to <target_directory>/xxxxx
Downloading... : 20/20 labels has been downloaded. 0 failed.
3. Complete downloading all labels and data.
```

The result is saved to the designated directory. For example:

```
└─ <target directory>
   ├─ project.json
   └─ my-dataset
      ├─ 1.jpg
      ├─ 1.jpg.json
      ├─ 2.jpg
      ├─ 2.jpg.json
      ...
```

You can view the help menu by using the '--help' option.

```bash
$ superb download --help
Usage: python -m spb_cli download [OPTIONS]

  Download all data and labels of your project in Superb Platform

Options:
  -d, --dir TEXT              Target directory path (default=[./])
  -p, --project TEXT          Target project name
  -y, --yes                   Say YES to all prompts
  -np, --num_process INTEGER  Number of processors for executing commands
                              (default=2)
  --help                      Show this message and exit.
```

## Contributing

Feel free to report issues and suggest improvements.  
Please email us at <support@superb-ai.com>

## License

The MIT License (MIT)

Copyright (c) 2020, Superb AI, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
