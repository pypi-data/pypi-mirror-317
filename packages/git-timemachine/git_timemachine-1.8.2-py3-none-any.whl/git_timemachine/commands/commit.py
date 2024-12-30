import random
from datetime import datetime, timedelta
from typing import List

import click
# pylint: disable=no-name-in-module
from pygit2 import discover_repository, Repository, GitError

from git_timemachine.types import ListParamType
from git_timemachine.git import check_commit_time, check_commit_status, check_max_daily_commits
from git_timemachine.git import git_external_commit, create_repo_commit, print_commit_details


@click.command('commit')
@click.option('-t', '--commit-time', help='Time node to commit with', type=click.DateTime(formats=['%Y-%m-%dT%H:%M:%S%z']), metavar='DATETIME')
@click.option('-m', '--message', help='Message describing the commit', type=str, required=True)
@click.option('-r', '--random-range', help='Random range of offset', type=ListParamType(length=2, item_type=int), default=[600, 3600])
@click.option('-e', '--external', help='Use external git command to commit', type=bool, is_flag=True, default=False)
@click.option('--max-daily-commits', help='Number of maximum daily commits.', type=int, metavar='N')
@click.argument('args', nargs=-1)
@click.pass_context
# pylint: disable=too-many-arguments
def commit_command(ctx: click.Context, commit_time: datetime, message: str, random_range: List[int], external: bool, max_daily_commits: int, args: List[str]):
    """Record a commit on repository at the specified time node."""

    repo_dir = ctx.obj['repo_dir']
    states = ctx.obj['states']
    config = ctx.obj['config']

    if commit_time is None:
        commit_time = states.get('commit-time', datetime.now().isoformat())

    if max_daily_commits is None:
        max_daily_commits = config['max-daily-commits']

    repo = Repository(discover_repository(repo_dir))

    try:
        check_commit_time(repo, commit_time)
        check_commit_status(repo)
        check_max_daily_commits(repo, commit_time, max_daily_commits)
    except GitError as exc:
        ctx.fail(str(exc))

    random.seed()
    commit_time += timedelta(seconds=random.randint(random_range[0], random_range[1]))

    if external:
        args = list(args)
        args += ['--message', message]
        git_external_commit(repo, args, commit_time)
    else:
        try:
            print_commit_details(create_repo_commit(repo, repo.default_signature.name, repo.default_signature.email, commit_time, message))
        except GitError as exc:
            ctx.fail(str(exc))

    ctx.obj['states'].set('commit-time', commit_time)
