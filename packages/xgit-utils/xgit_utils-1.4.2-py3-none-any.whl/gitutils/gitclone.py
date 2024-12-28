# -*- coding: utf-8 -*-
import os
import sys

import click

import gitutils
from gitutils import GitX, utils, GitRepo


class Clonex(GitX):
    """Clonex."""

    def __init__(self, target_dir: str, use_proxy: bool, proxy: str):
        super().__init__(target_dir=target_dir, use_proxy=use_proxy, proxy=proxy)

    def __run_clone(self, repo: GitRepo, prefix: str):
        """run clone

        Args:
            repo (gitutils.GitRepo): repo
            prefix (str): prefix
        """
        utils.my_print(f">> {utils.Color.green(prefix)} begin to clone {utils.Color.red(repo.name)} from {repo.url}")

        group_path = os.path.join(self.target_dir, repo.group)
        os.makedirs(group_path, exist_ok=True)

        repo_path = os.path.join(group_path, f"{repo.name}.git")

        if os.path.exists(repo_path):
            utils.my_print_red(">> Repo already exists")
            return

        GitX.exec_clone(group_path=group_path, url=repo.url)

    def clone_repo_list(self, repo_list: list[str], ignore: bool = False):
        """clone repo list

        Args:
            repo_list (list[str]): repo list
            ignore (bool, optional): add ignore. Defaults to False.
        """
        ignore_list: list[str] = []

        if not os.path.exists(gitutils.XGIT):
            os.makedirs(gitutils.XGIT)

        if os.path.exists(gitutils.XGIT_IGNORE):
            with open(gitutils.XGIT_IGNORE, "r") as f:
                lines = f.readlines()
                if lines and len(lines) > 0:
                    for line in lines:
                        ignore_list.append(line.strip())

        if ignore:
            for repo in repo_list:
                if not (repo.rstrip("/") in ignore_list):
                    ignore_list.append(repo.rstrip("/"))
            with open(gitutils.XGIT_IGNORE, "w") as f:
                f.writelines([line + "\n" for line in ignore_list])
            utils.my_print_green("Done")
            return

        filter_list: list[GitRepo] = [
            GitX.parse_git_url(item) for item in repo_list if not any(url in item for url in ignore_list)
        ]
        filter_list = [
            item
            for item in filter_list
            if not os.path.exists(os.path.join(self.target_dir, item.group, f"{item.name}.git"))
        ]
        self.__clone_repos(filter_list)

    def clone_url_file(self, url_file: str, ignore: bool = False):
        """repo clone

        Args:
            url_file (str): git url or file path
            ignore (bool, optional): add ignore. Defaults to False.
        """
        repo_list: list[str] = []

        if url_file.startswith("http") or url_file.startswith("git"):
            repo_list.append(url_file.strip())
        else:
            url_file = utils.abs_path(url_file.strip())
            if os.path.exists(url_file) and os.path.isfile(url_file):
                with open(url_file, "r") as f:
                    lines = f.readlines()
                    if lines and len(lines) > 0:
                        for line in lines:
                            repo_list.append(line.strip())

        self.clone_repo_list(repo_list=repo_list, ignore=ignore)

    def __clone_repos(self, repos: list[GitRepo]):
        """clone repos

        Args:
            repos (list[gitutils.GitRepo]): repo list
        """
        size: int = len(repos)
        if size > 0:
            for index, repo in enumerate(repos):
                self.__run_clone(repo, prefix="[{0}/{1}]".format(index + 1, size))
            utils.my_print_green(message="Done")
        else:
            utils.my_print_red(message="Exist")


@click.command(name="clone", help=f"Clone Git repositories. Version: {gitutils.__version__}", epilog="make it easy")
@click.option("--ignore", help="Skip cloning if the repository ignore", is_flag=True, default=False, show_default=True)
@click.argument("url_file", required=True, type=str)
@gitutils.options_proxy
@gitutils.options_target_dir
def cli_clone(url_file: str, target_dir: str, ignore: bool, use_proxy: bool, proxy: str):
    try:
        clonex = Clonex(target_dir=target_dir, use_proxy=use_proxy, proxy=proxy)
        clonex.clone_url_file(url_file=url_file, ignore=ignore)
    except Exception as e:
        utils.my_print_red(f"{e}")
    except KeyboardInterrupt:
        utils.my_print_red("Cancel")


def test():
    """
    test
    :return:
    """
    sys.argv.append("-u")
    # sys.argv.append("--ignore")
    sys.argv.append("~/Desktop/git.txt")


if __name__ == "__main__":
    test()
    cli_clone()
