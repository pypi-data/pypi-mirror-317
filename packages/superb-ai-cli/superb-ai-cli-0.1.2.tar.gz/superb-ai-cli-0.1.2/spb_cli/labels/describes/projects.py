import click
import math

from spb_cli.labels.base_service import BaseService
from spb_cli.labels.utils import (
    print_table
)


class ProjectService(BaseService):
    def show_projects(
        self,
        show_options,
        data_type,
        project_name,
    ):
        supported_options = ["default", "reviews"]
        if show_options not in supported_options:
            raise ValueError(
                f"show_options must be one of {supported_options}"
            )
        supported_data_types = ["all", "image", "video", "pointcloud"]
        if data_type not in supported_data_types:
            raise ValueError(
                f"data_type must be one of {supported_data_types}"
            )

        page = 1
        if show_options == "reviews":
            print_table([
                ["INR", "IN PROGRESS : Rejected"],
                ["INN", "IN PROGRESS : Not Submitted"],
                ["SUA", "SUBMITTED : Approved"],
                ["SUP", "SUBMITTED : Pending Review"],
                ["SKA", "SKIPPED : Approved"],
                ["SKP", "SKIPPED : Pending Review"],
            ])
            click.echo("\n")
        while True:
            count, projects = self.client.get_projects(
                page=page,
                name_icontains=project_name,
            )
            if show_options == "default":
                self.print_projects_default_option(
                    projects
                )
            else:
                self.print_projects_reviews_option(
                    projects
                )
            total_page = math.ceil(count / 10)
            if total_page > page:
                click.echo(
                    f"Press any button to continue to the next page ({page}/{total_page}). Otherwise press ‘Q’ to quit.",
                    nl=False,
                )
                key = click.getchar()
                click.echo("\n")
                page = page + 1
                if key == "q" or key == "Q":
                    return
            elif total_page == page:
                return

    def print_projects_default_option(self, projects):
        data = []
        data.append([
            "NAME",
            "DATA_TYPE",
            "LABELS",
            "IN_PROGRESS",
            "SUBMITTED",
            "SKIPPED"
        ])
        for project in projects:
            in_progress_ratio = (
                math.ceil(
                    project.in_progress_label_count / project.label_count * 100
                )
                if project.label_count > 0
                else 0
            )
            skipped_ratio = (
                math.ceil(
                    project.skipped_label_count / project.label_count * 100
                )
                if project.label_count > 0
                else 0
            )
            data.append(
                [
                    project.name,
                    project.workapp.split("-")[0],
                    project.label_count,
                    f"{project.in_progress_label_count} ({in_progress_ratio} %)",
                    f"{project.submitted_label_count} ({project.progress} %)",
                    f"{project.skipped_label_count} ({skipped_ratio} %)",
                ]
            )
        print_table(data)

    def print_projects_reviews_option(
        self, projects
    ):
        data = []
        data.append([
            "NAME",
            "DATA_TYPE",
            "LABELS",
            "INR",
            "INN",
            "SUA",
            "SUP",
            "SKA",
            "SKP"
        ])
        for project in projects:
            stats = project.stats if project.stats is not None else []

            in_progress_count = (
                [item for item in stats if item["type"] == "IN_PROGRESS_COUNT"][0:1]
                or [{}]
            )[0].get("info", {})
            submitted_count = (
                [item for item in stats if item["type"] == "SUBMITTED_COUNT"][0:1]
                or [{}]
            )[0].get("info", {})
            skipped_count = (
                [item for item in stats if item["type"] == "SKIPPED_COUNT"][0:1] or [{}]
            )[0].get("info", {})

            data.append([
                project.name,
                project.workapp.split("-")[0],
                f"{project.label_count}",
                f'{in_progress_count.get("rejected", 0)}',
                f'{in_progress_count.get("not_submitted", 0)}',
                f'{submitted_count.get("approved", 0)}',
                f'{submitted_count.get("pending_review", 0)}',
                f'{skipped_count.get("approved", 0)}',
                f'{skipped_count.get("pending_review", 0)}',
            ])
        print_table(data)
