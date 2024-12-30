from datetime import datetime, timezone, timedelta
from pathlib import Path

import click
# pylint: disable=no-name-in-module
from pygit2 import discover_repository, init_repository, Repository, Commit, GitError, GIT_SORT_REVERSE, GIT_DIFF_REVERSE, GIT_DIFF_SHOW_BINARY, \
    GIT_APPLY_LOCATION_BOTH

from git_timemachine.git import create_repo_commit, git_external_commit, git_external_migrate


@click.command('migrate')
@click.option('-e', '--external', help='Use external git command to commit', type=bool, is_flag=True, default=False)
@click.argument('dest_dir', type=click.Path(exists=False, file_okay=False), required=False, default=None)
@click.pass_context
def migrate_command(ctx: click.Context, external: bool, dest_dir: str):
    """Migrate commits to another repository."""

    repo_dir = Path(ctx.obj['repo_dir'])

    if dest_dir is None:
        dest_dir = repo_dir.parent.joinpath(repo_dir.name + '.migrate')
    else:
        dest_dir = Path(dest_dir)

    if dest_dir.exists():
        ctx.fail(f'Destination directory {dest_dir} already exists.')

    dest_dir.mkdir(0o755)

    src_repo = Repository(discover_repository(str(repo_dir)))
    dest_repo = init_repository(dest_dir, initial_head='main')

    for commit in src_repo.walk(src_repo.head.target, GIT_SORT_REVERSE):
        commit_time = datetime.fromtimestamp(commit.author.time, tz=timezone(timedelta(minutes=commit.author.offset)))

        if external:
            git_external_migrate(str(repo_dir), str(dest_dir), commit.id.hex)

            git_external_commit(dest_repo, ['--message', commit.message], commit_time)
        else:
            try:
                apply_commit_diff(dest_repo, commit)
                create_repo_commit(dest_repo, commit.author.name, commit.author.email, commit_time, commit.message)
            except GitError as exc:
                ctx.fail(str(exc))


def apply_commit_diff(repo: Repository, commit: Commit):
    if len(commit.parents) > 0:
        diff = commit.tree.diff_to_tree(commit.parents[0].tree, flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)
    else:
        diff = commit.tree.diff_to_tree(flags=GIT_DIFF_REVERSE | GIT_DIFF_SHOW_BINARY)

    repo.apply(diff, location=GIT_APPLY_LOCATION_BOTH)
    repo.index.write()

    tree = repo.index.write_tree()

    if tree is None:
        raise GitError('Failed to write index tree.')
