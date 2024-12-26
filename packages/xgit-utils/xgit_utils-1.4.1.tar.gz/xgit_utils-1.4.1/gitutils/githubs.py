# -*- coding: utf-8 -*-
import os

import click
from github import Github

from github import Auth

import gitutils
from gitutils.gitclone import Clonex
from gitutils import GitX


class GithubX(GitX):
    """Github X."""

    def __init__(self, use_proxy: bool, proxy: str, token: str = None):
        super().__init__(target_dir=None, use_proxy=use_proxy, proxy=proxy)
        self.token = token

    def __init_github(self) -> Github:
        if self.token is None:
            raise ValueError(
                "A GitHub token must be provided either as a parameter or in the 'GITHUB_TOKEN' environment variable."
            )
        return Github(auth=Auth.Token(self.token))

    def get_starred(self) -> list[str]:
        github = self.__init_github()
        try:
            return [repo.clone_url for repo in github.get_user().get_starred()]
        finally:
            github.close()

    def get_repos(self) -> list[str]:
        github = self.__init_github()
        try:
            return [repo.clone_url for repo in github.get_user().get_repos()]
        finally:
            github.close()

    def get_repos_by_user(self, user: str = "hyxf") -> list[str]:
        github = self.__init_github()
        try:
            return [repo.clone_url for repo in github.get_user(login=user).get_repos()]
        finally:
            github.close()


def output_repos(export: bool, repos: list[str]):
    if export:
        output_file = GitX.export_txt(content="\n".join(repos), filename="github_repos")
        click.echo(f"Repositories[{len(repos)}] have been written to {output_file}.")
    else:
        click.echo(f"Repositories[{len(repos)}]:")
        for repo in repos:
            click.echo(repo)


@click.command(
    name="github", help=f"Manage GitHub repositories. Version: {gitutils.__version__}", epilog="make it easy"
)
@click.option(
    "-t",
    "--token",
    default=os.getenv("GITHUB_TOKEN"),
    show_default=os.getenv("GITHUB_TOKEN"),
    help="GitHub personal access token.",
)
@click.option("--clone", is_flag=True, help="Clone all repositories from the specified user or organization.")
@click.option("--mine", is_flag=True, help="List your own repositories.")
@click.option("--user", type=str, default=None, help="List repositories for the specified user.")
@click.option("--export", is_flag=True, help="Export the repository list to a file.")
@gitutils.options_proxy
@gitutils.options_target_dir
def cli_github(
    target_dir: str, token: str, clone: bool, mine: bool, user: str, export: bool, use_proxy: bool, proxy: str
):
    try:
        click.echo("Running")
        githubx = GithubX(token=token, use_proxy=use_proxy, proxy=proxy)
        if mine:
            repos = githubx.get_repos()
        elif user:
            repos = githubx.get_repos_by_user(user=user)
        else:
            repos = githubx.get_starred()
        if clone:
            clonex = Clonex(target_dir=target_dir, use_proxy=use_proxy, proxy=proxy)
            clonex.clone_repo_list(repo_list=repos)
        else:
            output_repos(export=export, repos=repos)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)


if __name__ == "__main__":
    # sys.argv.append("--mine")
    # sys.argv.append("-u")
    # sys.argv.append("--output-file")
    # sys.argv.append("~/Desktop/git.txt")
    cli_github()
