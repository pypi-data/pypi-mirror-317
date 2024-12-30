from datetime import timedelta, datetime

import click


@click.command('switch-date')
@click.option('-d', '--days', help='Days to switch for commit time.', type=int, default=1)
@click.option('-h', '--begin-hour', help='Hour to begin with.', type=int, default=10)
@click.argument('target_date', metavar='DATE', type=str, required=False)
@click.pass_context
def switch_date_command(ctx: click.Context, days: int, begin_hour: int, target_date: str):
    """Switch the commit time of states."""

    states = ctx.obj['states']

    if target_date is None:
        commit_time = states.get('commit-time') + timedelta(hours=days * 24)
    else:
        commit_time = datetime.fromisoformat(target_date)

    states.set('commit-time', commit_time.replace(hour=begin_hour, minute=0, second=0, microsecond=0))
