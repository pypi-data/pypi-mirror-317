import click

import gitutils
from gitutils.gitclone import cli_clone
from gitutils.githubs import cli_github
from gitutils.gitsync import cli_sync


@click.group(name="xgit", help=f"Git repository management tool {gitutils.__version__}", epilog="make it easy.")
def cli():
    pass


cli.add_command(cli_clone)
cli.add_command(cli_github)
cli.add_command(cli_sync)

if __name__ == "__main__":
    cli()
