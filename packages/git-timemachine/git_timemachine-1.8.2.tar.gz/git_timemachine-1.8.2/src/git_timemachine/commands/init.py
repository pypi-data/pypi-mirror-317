from datetime import datetime
from pathlib import Path

import click
import ini


@click.command('init')
@click.pass_context
def init_command(ctx: click.Context):
    """Initialize states and configurations for git-timemachine."""

    states = ctx.obj['states']
    config_file = Path(ctx.obj['config_file'])

    states.set('commit-time', datetime.now())

    config_file.parent.mkdir(0o755, exist_ok=True)
    config_file.write_text(ini.stringify({'max-daily-commits': 5}), encoding='utf-8')
