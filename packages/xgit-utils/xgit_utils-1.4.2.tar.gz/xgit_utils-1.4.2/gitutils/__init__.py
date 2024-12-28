# -*- coding: utf-8 -*-
import configparser
import os
import re
from dataclasses import dataclass
import shutil
import time
from urllib import parse

import click

from gitutils import utils

__version__ = "1.4.2"

DEFAULT_PROXY = "127.0.0.1:1087"
DEFAULT_GITHUB = os.path.expanduser("~/Mirror/github")
XGIT = os.path.expanduser("~/.xgit")
XGIT_IGNORE = os.path.join(XGIT, ".xgitignore")
DEFAULT_THREAD_SIZE = 6


def options_proxy(func):
    func = click.option("-u", "--use-proxy", is_flag=True, help="use proxy")(func)
    func = click.option("-p", "--proxy", type=str, default=DEFAULT_PROXY, show_default=True, help="http[s] proxy")(func)
    return func


def options_target_dir(func):
    func = click.option(
        "-d",
        "--target-dir",
        type=str,
        default=DEFAULT_GITHUB,
        show_default=True,
        help="Specify the target directory for mirrored repositories.",
    )(func)
    return func


@dataclass
class GitRepo:
    url: str
    host: str
    path: str | None
    name: str | None = None
    group: str | None = None


class GitX:
    """GitX."""

    def __init__(self, target_dir: str, use_proxy: bool, proxy: str):
        self.target_dir = target_dir
        self.use_proxy = use_proxy
        self.proxy = proxy
        self.set_proxy()
        self.git_check()

    def git_check(self):
        git_path = shutil.which("git")
        if git_path is None:
            raise FileNotFoundError("Git command not found, please install git first.")

    def set_proxy(self):
        if self.use_proxy and self.proxy:
            if utils.is_connected(url=self.proxy):
                os.environ.setdefault(key="http_proxy", value="http://{}".format(self.proxy))
                os.environ.setdefault(key="https_proxy", value="http://{}".format(self.proxy))

    @staticmethod
    def exec_fetch(repo_dir: str):
        os.chdir(repo_dir)
        os.system("git fetch origin")

    @staticmethod
    def exec_clone(group_path: str, url: str):
        os.chdir(group_path)
        cmd_clone_mirror = f"git clone --mirror {url}"
        os.system(cmd_clone_mirror)

    @staticmethod
    def parse_host(url: str) -> str | None:
        parsed_url = parse.urlparse(url) if url else None
        if parsed_url and parsed_url.hostname:
            return parsed_url.hostname

        ssh_pattern = r"^(?:git@)([^:]+):.*$"
        match = re.match(ssh_pattern, url)
        if match:
            return match.group(1)

        return None

    @staticmethod
    def parse_git_url(git_url: str) -> GitRepo:
        url = git_url
        if url.startswith("git@"):
            url = url.replace(":", "/").replace("git@", "https://")

        parse_result = parse.urlparse(url)
        hostname = parse_result.hostname.strip()

        parse_path = parse_result.path.rstrip("/")
        if parse_path.endswith(".git"):
            parse_path = parse_path[:-4]

        paths = [x for x in parse_path.split("/") if x]

        if len(paths) < 2:
            raise ValueError("The 'git URL' format is incorrect")

        group, name = paths[0], paths[1]

        if hostname == "github.com" and not url.endswith(".git"):
            url = url.rstrip("/") + ".git"

        if not git_url.startswith("git@"):
            git_url = url

        return GitRepo(url=git_url, group=group, host=hostname, name=name, path=None)

    @staticmethod
    def parse_url(file_path: str) -> str:
        config = configparser.ConfigParser()
        config.read(file_path)
        try:
            return config['remote "origin"']["url"]
        except KeyError:
            return ""

    @staticmethod
    def export_txt(content: str, filename: str = "repo") -> str:
        current_time = time.strftime("%Y%m%d%H%M%S")
        export_file = os.path.join(os.getcwd(), f"{filename}-{current_time}.txt")

        with open(export_file, "w") as f:
            f.write(content.strip())

        return export_file

    @staticmethod
    def scan_repo(root_dir: str, filter_host: list[str] = None) -> list[GitRepo]:
        if not os.path.isdir(root_dir):
            return []

        desired_dirs: list[GitRepo] = []

        for root, dirs, files in os.walk(root_dir):
            if ".git" in dirs or ".svn" in dirs:
                dirs[:] = []
                continue

            if "refs" in dirs and "objects" in dirs:
                conf_path = os.path.join(root, "config")
                url = GitX.parse_url(conf_path) if os.path.isfile(conf_path) else ""
                host = GitX.parse_host(url)
                if filter_host and len(filter_host) > 0:
                    if host in filter_host:
                        desired_dirs.append(GitRepo(path=root, url=url, host=host))
                else:
                    desired_dirs.append(GitRepo(path=root, url=url, host=host))
                dirs[:] = []
            else:
                dirs[:] = [d for d in dirs if d not in {"refs", "objects"}]

        return desired_dirs
