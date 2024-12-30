import os
from pathlib import Path

import click
import ini

from git_timemachine import __version__
from git_timemachine.commands import command_group
from git_timemachine.utils import StateManager
from git_timemachine.config import default


def print_version(ctx: click.Context, _, value: str):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group(commands=command_group)
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('-C', '--repo-dir', help='Path of repository directory.', type=click.Path(exists=True, file_okay=False), default=os.getcwd(), metavar='REPO')
@click.option('--states-dir', help='Path of states directory.', type=click.Path(file_okay=False, exists=False), is_eager=True,
              default=Path.home().joinpath('.cache', 'git-timemachine', 'states'))
@click.option('--config-file', help='Path of configuration file', type=click.Path(dir_okay=False, exists=False), is_eager=True,
              default=Path.home().joinpath('.config', 'git-timemachine', 'config.ini'))
@click.pass_context
def cli(ctx: click.Context, repo_dir: str, states_dir: str, config_file: str):
    """A command-line tool that helps you record commits on Git repositories at any time node."""

    ctx.ensure_object(dict)
    ctx.obj['repo_dir'] = repo_dir
    ctx.obj['states'] = StateManager(states_dir)
    ctx.obj['config_file'] = config_file

    config = default.copy()

    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as fp:
            config.update(ini.parse(fp.read()))

    ctx.obj['config'] = config


if __name__ == '__main__':  # pragma: no cover
    cli()  # pylint: disable=no-value-for-parameter
