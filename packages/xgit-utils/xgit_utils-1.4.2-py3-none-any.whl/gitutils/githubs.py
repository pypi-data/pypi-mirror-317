# -*- coding: utf-8 -*-
import json
import os
import sys
import time
from typing import Optional

import click
from github import Github

from github.Repository import Repository
from github.PaginatedList import PaginatedList

from github import Auth

import gitutils
from gitutils import utils
from gitutils.gitclone import Clonex
from gitutils import GitX
from pydantic import BaseModel


class GithubRepo(BaseModel):
    id: int
    name: str
    description: Optional[str]
    html_url: str
    clone_url: str
    language: Optional[str]
    last_modified: str
    stargazers_count: int
    login: str
    avatar_url: str
    login_html_url: str


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

    def get_starred(self) -> PaginatedList[Repository]:
        github = self.__init_github()
        try:
            return github.get_user().get_starred()
            # return [repo.clone_url for repo in repos]
        finally:
            github.close()

    def get_repos(self) -> PaginatedList[Repository]:
        github = self.__init_github()
        try:
            return github.get_user().get_repos()
            # return [repo.clone_url for repo in github.get_user().get_repos()]
        finally:
            github.close()

    def get_repos_by_user(self, user: str = "hyxf") -> PaginatedList[Repository]:
        github = self.__init_github()
        try:
            return github.get_user(login=user).get_repos()
        finally:
            github.close()


def get_last_modified(repo: Repository) -> str:
    if repo.last_modified_datetime is not None:
        return repo.last_modified_datetime.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return repo.created_at.strftime("%Y-%m-%d %H:%M:%S")


def output_repos(export: bool, repos: PaginatedList[Repository]):
    if export:
        repo_list = [
            GithubRepo(
                id=repo.id,
                name=repo.name,
                description=repo.description,
                html_url=repo.html_url,
                clone_url=repo.clone_url,
                language=repo.language,
                last_modified=get_last_modified(repo),
                stargazers_count=repo.stargazers_count,
                login=repo.owner.login,
                avatar_url=repo.owner.avatar_url,
                login_html_url=repo.owner.html_url,
            )
            for repo in repos
        ]
        json_string = json.dumps(
            [repo.model_dump(exclude_unset=True, exclude_none=True) for repo in repo_list],
            separators=(",", ":"),
            ensure_ascii=False,
        )
        script_string = f"window.__DATA__ = {json_string}"

        with open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "templates", "index.html"), "r", encoding="utf-8"
        ) as file:
            html_content = file.read()

        current_time = time.strftime("%Y%m%d%H%M%S")
        export_file = os.path.join(os.getcwd(), f"repos-{current_time}.html")

        utils.insert_script_to_html(html_content, script_string, export_file)
        click.echo(f"Repositories[{repos.totalCount}] have been written to {export_file}.")
    else:
        click.echo(f"Repositories[{repos.totalCount}]:")
        for repo in repos:
            click.echo(repo.clone_url)


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
            clonex.clone_repo_list(repo_list=[repo.clone_url for repo in repos])
        else:
            output_repos(export=export, repos=repos)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)


if __name__ == "__main__":
    sys.argv.append("--mine")
    sys.argv.append("-u")
    sys.argv.append("--export")
    # sys.argv.append("--output-file")
    # sys.argv.append("~/Desktop/git.txt")
    cli_github()
