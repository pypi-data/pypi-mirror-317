import sys
import json
from typing import Iterable
from functools import reduce

import click
import yaml
from pygit2 import discover_repository, Repository, Commit  # pylint: disable=no-name-in-module


@click.command('log')
@click.option('-f', '--format', 'output_format', help='Output format.',
              type=click.Choice(['json', 'yaml']), default='json')
@click.option('--check', help='Check author and commit time', type=bool, is_flag=True, default=False)
@click.pass_context
def log_command(ctx: click.Context, output_format: str, check: bool):
    """Show commit logs of a repository in the specified format."""

    repo_dir = ctx.obj['repo_dir']

    repo = Repository(discover_repository(repo_dir))
    commits = repo.walk(repo.head.target)

    if check:
        if not reduce(lambda prev, current: prev and current, map(check_commit_consistence, commits), True):
            sys.exit(1)
    else:
        dump_commit_logs(commits, output_format)


def dump_commit_logs(commits: Iterable[Commit], output_format: str):
    logs = [{
        'id': commit.id.hex,
        'tree_id': commit.tree_id.hex,
        'parents': [parent.id.hex for parent in commit.parents],
        'author': {
            'name': commit.author.name,
            'email': commit.author.email,
            'time': commit.author.time,
            'offset': commit.author.offset
        },
        'committer': {
            'name': commit.committer.name,
            'email': commit.committer.email,
            'time': commit.committer.time,
            'offset': commit.committer.offset
        },
        'gpg': None if commit.gpg_signature[0] is None else [gpg.decode('utf-8') for gpg in commit.gpg_signature],
        'message': commit.message
    } for commit in commits]

    if output_format == 'yaml':
        yaml.dump(logs, sys.stdout)
    else:
        json.dump(logs, sys.stdout, ensure_ascii=False, indent=4)


def check_commit_consistence(commit: Commit) -> bool:
    output = []

    if commit.author.name != commit.committer.name:
        output.append(f'[{commit.id.hex}][name] author: {commit.author.name}, committer: {commit.committer.name}')

    if commit.author.email != commit.committer.email:
        output.append(f'[{commit.id.hex}][email] author: {commit.author.email}, committer: {commit.committer.email}')

    if commit.author.time != commit.committer.time:
        output.append(f'[{commit.id.hex}][time] author: {commit.author.time}, committer: {commit.committer.time}')

    if commit.author.offset != commit.committer.offset:
        output.append(f'[{commit.id.hex}][offset] author: {commit.author.offset}, committer: {commit.committer.offset}')

    if len(output) > 0:
        click.echo('\n'.join(output), err=True)
        return False

    return True
