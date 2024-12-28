# -*- coding: utf-8 -*-
import os
import platform
import socket
import time
from dataclasses import dataclass
from time import gmtime
from time import strftime


def insert_script_to_html(html_string: str, script_string: str, output_file: str = "output.html"):
    script_tag = f"<script>\n{script_string}\n</script>"
    modified_html = None
    if "</body>" in html_string:
        modified_html = html_string.replace("</body>", f"    {script_tag}\n</body>")
    elif "<head>" in html_string and "</head>" in html_string:
        modified_html = html_string.replace("<head>", f"<head>\n    {script_tag}")
    else:
        modified_html = html_string.strip() + f"\n{script_tag}"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(modified_html)


def is_connected(url: str) -> bool:
    try:
        hostname = url.split(":")[0]
        port = int(url.split(":")[1])
        socket.create_connection((hostname, port))
        return True
    except OSError:
        pass
    return False


def abs_path(path):
    if path.startswith("~"):
        path = os.path.expanduser(path)
    return os.path.abspath(path)


def mac_notify(content: str, title: str):
    os.system('osascript -e \'display notification "{0}" with title "{1}"\''.format(content, title))


def time_count(count) -> str:
    return strftime("%H:%M:%S", gmtime(count))


def is_root() -> bool:
    return os.geteuid() == 0


def is_mac() -> bool:
    return platform.system() == "Darwin"


def my_print(message: str):
    print(Color.green(time.strftime("%Y-%m-%d %H:%M:%S -")), message)


def my_print_red(message: str):
    print(Color.red(time.strftime("%Y-%m-%d %H:%M:%S -")), Color.red(message))


def my_print_green(message: str):
    print(Color.green(time.strftime("%Y-%m-%d %H:%M:%S -")), Color.green(message))


class Color(object):
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BlUE = "\033[94m"
    END = "\033[0m"

    @classmethod
    def red(cls, string):
        return cls.RED + string + cls.END

    @classmethod
    def green(cls, string):
        return cls.GREEN + string + cls.END

    @classmethod
    def yellow(cls, string):
        return cls.YELLOW + string + cls.END

    @classmethod
    def blue(cls, string):
        return cls.BlUE + string + cls.END


@dataclass
class Folder:
    path: str
    size: int
    mess: str
    url: str


def folder_size(folder: str, url: str) -> Folder:
    total_size = 0
    for root, dirs, filenames in os.walk(folder):
        for f in filenames:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total_size += os.path.getsize(fp)

    size_mb = total_size / (1024 * 1024)
    return Folder(path=folder, size=total_size, mess=f"{size_mb:.2f} MB", url=url)


if __name__ == "__main__":
    folder = folder_size("/Users/seven/Mirror/github/git/git.git")
    print(f"{folder.mess}-{folder.size}")
