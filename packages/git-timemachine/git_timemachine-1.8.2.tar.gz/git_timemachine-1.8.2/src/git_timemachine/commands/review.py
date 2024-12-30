from datetime import datetime

import click
from tabulate import tabulate

# pylint: disable=no-name-in-module
from pygit2 import Repository, discover_repository


@click.command('review')
@click.pass_context
def review_command(ctx: click.Context):
    """Review commits of repository."""

    repo_dir = ctx.obj['repo_dir']

    repo = Repository(discover_repository(str(repo_dir)))
    report = {}

    for commit in repo.walk(repo.head.target):
        date_str = datetime.fromtimestamp(commit.commit_time).strftime('%Y-%m-%d')

        if date_str in report:
            report[date_str] += 1
        else:
            report[date_str] = 1

    click.echo(tabulate([[key, value] for key, value in report.items()], headers=['date', 'commits']))
