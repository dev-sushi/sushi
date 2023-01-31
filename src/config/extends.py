"""sushi 0.1"""

import configparser
import os
import platform
import tempfile
from pathlib import Path
from shutil import rmtree

from git import Repo
from rich import print as rich_print

# pylint: disable=import-error, too-few-public-methods
from src.cache.main import Cache

# pylint: enable=import-error

config = configparser.ConfigParser()
config.read("sushi.conf")

# get temp and current path
tempdir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
currentpath = os.path.dirname(os.path.realpath(__file__))


class ConfigExtends:
    """extends config from another config"""

    def _parse_repo(self, repo: str) -> dict[str, str]:
        """parse repo config

        example:
        from: `@dev-sushi/example`
        to: `https://github.com/dev-sushi/example`
        """

        # this string contains 2 parts: user, repository name seperated with /
        newrepo = repo.replace("@", "")
        split: str = newrepo.split("/")
        return {"user": split[0], "name": split[1]}

    def _get_repo(self, data: str, filename: str):
        repourl = f"https://github.com/{data.get('user')}/{data.get('name')}"

        rich_print("[bold yellow]sushi[/bold yellow]   cloning repository")

        # clone repository
        repo = Repo.clone_from(repourl, f"{tempdir}/sushi/")
        repo.git.checkout("main")

        # add new config to cache
        with open(f"{tempdir}/sushi/{filename}", "r", encoding="UTF-8") as f:
            Cache.update(
                Cache, "EXTENDS_CONFIG = None", f'EXTENDS_CONFIG = """{f.read()}"""'
            )

        rmtree(f"{tempdir}/sushi/")

    def install(self):
        """installs custom config"""

        repo: str = config["extends"]["repo"]
        filename: str = config["extends"]["file"]

        data = self._parse_repo(repo)
        self._get_repo(data, filename)
