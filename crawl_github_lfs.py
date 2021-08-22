#!/usr/bin/env python3

import click
import urllib.request
import json
import tempfile
import subprocess
from dataclasses import dataclass


@dataclass
class RepositoryInfo:
    html_url: str
    ssh_url: float


class GithubRepos:
    def __init__(self, username: str):
        self.username = username

    def __iter__(self):
        page = 0
        while True:
            page += 1
            with urllib.request.urlopen(f"https://api.github.com/users/{self.username}/repos?page={page}") as url:
                data = json.loads(url.read().decode())
                if not isinstance(data, list):
                    break
                if not data:
                    break
                for entry in data:
                    if isinstance(entry, dict):
                        if "html_url" in entry and "ssh_url" in entry:
                            yield RepositoryInfo(
                                html_url=entry["html_url"],
                                ssh_url=entry["ssh_url"]
                            )


@click.command()
@click.argument('username')
def main(username):
    for repo in GithubRepos(username):
        with tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None) as tmp_dir:
            print()
            print(f"== {repo.html_url} ==")
            subprocess.run(["git", "clone", repo.ssh_url, tmp_dir],
                           capture_output=True, cwd=tmp_dir, check=True)
            subprocess.run(["git", "lfs", "ls-files", "--all"],
                           capture_output=False, cwd=tmp_dir, check=True)

    print()


if __name__ == "__main__":
    main()
