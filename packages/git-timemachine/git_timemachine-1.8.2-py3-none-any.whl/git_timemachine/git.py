import os
import subprocess
from datetime import datetime
from typing import List

# pylint: disable=no-name-in-module
from pygit2 import Repository, Signature, GIT_STATUS_WT_NEW, Commit, GitError
from tabulate import tabulate


def git_external_commit(repo: Repository, args: List[str], commit_time: datetime):
    env = commit_time.replace(microsecond=0).astimezone().isoformat()

    subprocess.run(
        ['git', '-C', repo.workdir, 'commit'] + list(args),
        cwd=repo.workdir,
        env={**os.environ, 'GIT_AUTHOR_DATE': env, 'GIT_COMMITTER_DATE': env},
        check=True
    )


def git_external_migrate(src_dir: str, dest_dir: str, commit_id: str):
    result = subprocess.run(
        ('git', '-C', src_dir, 'show', '--binary', commit_id),
        cwd=src_dir,
        check=True,
        capture_output=True
    )

    subprocess.run(
        ('git', '-C', dest_dir, 'apply', '--allow-empty'),
        cwd=dest_dir,
        input=result.stdout,
        check=True
    )

    subprocess.run(
        ('git', '-C', dest_dir, 'add', '.'),
        cwd=dest_dir,
        check=True
    )


def create_repo_commit(repo: Repository, name: str, email: str, commit_time: datetime, message: str) -> Commit:
    parents = []

    if repo.head_is_unborn:
        try:
            git_config = repo.config.get_global_config()
            ref_name = git_config['init.defaultBranch'] if 'init.defaultBranch' in git_config else 'main'
        except OSError:
            ref_name = 'main'

        ref_name = f'refs/heads/{ref_name}'
    else:
        parents.append(repo.head.target)
        ref_name = repo.head.name

    signature = Signature(
        name=name,
        email=email,
        time=int(commit_time.replace(microsecond=0).timestamp()),
        encoding='utf-8',
        offset=0 if commit_time.tzinfo is None else int(commit_time.tzinfo.utcoffset(commit_time).seconds / 60)
    )

    tree = repo.index.write_tree()
    if tree is None:
        raise GitError('Failed to write index tree.')

    oid = repo.create_commit(ref_name, signature, signature, message, tree, parents)

    if oid is None:
        raise GitError('Failed to create commit.')

    return next(repo.walk(oid))


def check_max_daily_commits(repo: Repository, commit_time: datetime, max_num: int):
    if repo.head_is_unborn or max_num == 0:
        return

    date_str = commit_time.strftime('%Y-%m-%d')

    commits = [commit for commit in repo.walk(repo.head.target) if datetime.fromtimestamp(commit.commit_time).strftime('%Y-%m-%d') == date_str]

    if len(commits) >= max_num:
        raise GitError(f'Exceeded the daily commit limit: {max_num}.')


def check_commit_time(repo: Repository, commit_time: datetime):
    if not repo.head_is_unborn and commit_time.timestamp() < next(repo.walk(repo.head.target)).commit_time:
        raise GitError('Commit time is earlier than HEAD.')


def check_commit_status(repo: Repository):
    repo_status = repo.status(untracked_files='no')
    if repo_status == {} or len([value for value in repo_status.values() if value < GIT_STATUS_WT_NEW]) < 1:
        raise GitError('Nothing to commit or pending changes.')


def print_commit_details(commit: Commit):
    print(f'commit: {commit.id.hex}')
    print(f'author: {commit.author.name} <{commit.author.email}>')
    print(f'committer: {commit.committer.name} <{commit.committer.email}>')
    print(f'datetime: {datetime.fromtimestamp(commit.commit_time).astimezone().isoformat()}')
    print(f'message: {commit.message}')

    table = []
    if len(commit.parents) == 0:
        diff = commit.tree.diff_to_tree(swap=True)
    else:
        diff = commit.parents[0].tree.diff_to_tree(commit.tree)

    for patch in diff:
        table.append([
            patch.delta.status_char(),
            patch.delta.new_file.path,
            oct(patch.delta.new_file.mode & 0o100777)[2:] if patch.delta.status_char() != 'D' else ''
        ])

    print(tabulate(table, headers=['status', 'file', 'mode']))
