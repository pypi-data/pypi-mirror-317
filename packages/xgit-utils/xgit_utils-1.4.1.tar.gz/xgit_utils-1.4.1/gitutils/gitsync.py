# -*- coding: utf-8 -*-
import os
import sys
import time
from multiprocessing import Pool

import click
from tqdm import tqdm

from gitutils import GitRepo, GitX, utils
import gitutils


class SyncX(GitX):
    """docstring for SyncX."""

    def __init__(self, target_dir: str, use_proxy: bool, proxy: str):
        super().__init__(target_dir=target_dir, use_proxy=use_proxy, proxy=proxy)

    def repos_fetch(self, repo_list: list[GitRepo], thread_size: int):
        if thread_size <= 0:
            thread_size = 1
        pool = Pool(processes=thread_size)
        size = len(repo_list)
        for index, repo in enumerate(repo_list):
            pool.apply_async(self.repo_fetch, args=(repo.path, self.target_dir, size, index))
        pool.close()
        pool.join()

    def repo_fetch(self, repo: str, target_dir: str, size: int, index: int):
        utils.my_print("[{0}/{1}] - {2}".format(index + 1, size, repo.replace(target_dir, "")))
        GitX.exec_fetch(repo_dir=repo)

    def repo_sync(
        self,
        thread_size: int,
        filter_host: list[str] = None,
        list_remote: bool = False,
        list_repo: bool = False,
        repo: str = None,
        export: bool = False,
    ):
        if not os.path.exists(self.target_dir):
            os.makedirs(self.target_dir)

        """:type:str"""
        start_time = time.time()
        utils.my_print(">> Start: {0}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time))))

        repo_list = GitX.scan_repo(root_dir=self.target_dir, filter_host=filter_host)
        if list_remote:
            if not repo_list:
                utils.my_print_red(">> no repo")
                return

            remote_list: list[str] = []

            for repo in repo_list:
                if not (repo.host in remote_list):
                    remote_list.append(repo.host)

            size = len(remote_list)
            for index, host in enumerate(remote_list):
                utils.my_print("[{0}/{1}] - {2}".format(index + 1, size, host))

        elif list_repo:
            if not repo_list:
                utils.my_print_red(">> no repo")
                return

            folder_list = []

            for repo in tqdm(repo_list, desc="Processing", unit="items"):
                folder_list.append(utils.folder_size(repo.path, repo.url))

            folder_list.sort(key=lambda f: f.size)

            size = len(repo_list)
            for index, folder in enumerate(folder_list):
                utils.my_print("[{0}/{1}] - {2} - {3}".format(index + 1, size, folder.mess, folder.url))

        elif export:
            if not repo_list:
                utils.my_print_red(">> no repo")
                return

            size = len(repo_list)
            export_content = "\n".join([repo.url for repo in repo_list])

            export_file = GitX.export_txt(content=export_content, filename="repo")

            utils.my_print_green(f"export [{size}] repo - {export_file}")

        elif repo:
            repos: list[GitRepo] = []
            t_list = [x for x in repo.split(",") if x != ""]
            for x in repo_list:
                for y in t_list:
                    if x.url.lower().find(y.lower()) > -1:
                        repos.append(x)
                        break
            self.repos_fetch(repo_list=repos, thread_size=thread_size)
        else:
            self.repos_fetch(repo_list=repo_list, thread_size=thread_size)
        end_time = time.time()
        utils.my_print(">> End {0}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time))))
        run_time = int(end_time - start_time)
        utils.my_print(">> Time: {0}".format(utils.time_count(run_time)))


@click.command(
    name="sync",
    help=f"Synchronize local and remote Git repositories. Version: {gitutils.__version__}",
    epilog="make it easy",
)
@click.option(
    "-t",
    "--thread",
    type=int,
    default=gitutils.DEFAULT_THREAD_SIZE,
    show_default=True,
    help="Number of threads to use for synchronization.",
)
@click.option(
    "-f",
    "--filter-host",
    default=None,
    type=str,
    multiple=True,
    help="Filter repositories by host (supports multiple values).",
)
@click.option("--repo", type=str, help="Synchronize a specific repository.")
@click.option("--list-remote", is_flag=True, help="List all remote.")
@click.option("--list-repo", is_flag=True, help="List all local repositories.")
@click.option("--export", is_flag=True, help="Export the repository list to a file.")
@gitutils.options_proxy
@gitutils.options_target_dir
def cli_sync(
    target_dir: str,
    thread: int,
    filter_host: list[str],
    repo: str,
    list_remote: bool,
    list_repo: bool,
    export: bool,
    use_proxy: bool,
    proxy: str,
):
    try:
        sync = SyncX(target_dir=target_dir, use_proxy=use_proxy, proxy=proxy)
        sync.repo_sync(
            thread_size=thread,
            filter_host=filter_host,
            list_remote=list_remote,
            list_repo=list_repo,
            repo=repo,
            export=export,
        )
    except Exception as e:
        utils.my_print_red(f"{e}")
    except KeyboardInterrupt:
        utils.my_print_red("Cancel")


def test():
    sys.argv.append("-t")
    sys.argv.append("10")

    # sys.argv.append("-f")
    # sys.argv.append("github.com")

    # sys.argv.append("--list-repo")
    # sys.argv.append("--list-remote")

    sys.argv.append("--repo")
    sys.argv.append("okhttp")


if __name__ == "__main__":
    test()
    cli_sync()
