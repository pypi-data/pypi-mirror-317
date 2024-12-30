import click


@click.command('alias')
def alias_command():
    """Print alias commands for shell."""

    print('''alias gtm='git-timemachine'
alias gl='cat $HOME/.cache/git-timemachine/states/commit-time && echo'
alias ge='vim $HOME/.cache/git-timemachine/states/commit-time'
alias gn='gtm switch-date && gl'
alias gc='gtm commit -e -m'
alias gr='gtm review' ''')
