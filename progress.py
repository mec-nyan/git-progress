#!/usr/bin/env python3
"""
Git-progress

Check the status of multiple repositories at once.
"""

import os
import subprocess
import sys


def is_repo(path: str) -> bool:
    return os.path.isdir(os.path.join(path, ".git"))


def get_status(path: str) -> tuple[str, int]:
    branch = "N/A"
    changes = 0

    try:
        output = subprocess.check_output(
            ["git", "-C", path, "status", "--short", "--branch"],
            stderr=subprocess.DEVNULL,
            universal_newlines=True,
        )
        lines = output.strip().splitlines()
        if len(lines):
            branch = lines[0].split("...")[0].replace("##", "").strip()
            changes = len(lines) - 1

    except subprocess.CalledProcessError:
        ...

    return branch, changes


def get_it_all(path: str) -> list[dict]:
    out: list[dict] = []
    for entry in os.scandir(path):
        if entry.is_dir() and is_repo(entry.path):
            branch, changes = get_status(entry.path)
            out.append(
                {
                    "repo": entry.name,
                    "branch": branch or "Invalid repo",
                    "changes": changes,
                }
            )
    return out


if __name__ == "__main__":
    path = "."
    args = sys.argv
    if len(args) == 2:
        path = args[1]

    info = get_it_all(path)
    if not len(info):
        print("Nothing to see here")
        sys.exit(1)

    repo_w = 0
    branch_w = 0

    for line in info:
        if len(line["repo"]) > repo_w:
            repo_w = len(line["repo"])
        if len(line["branch"]) > branch_w:
            branch_w = len(line["branch"])

    for line in info:
        repo = line["repo"]
        branch = line["branch"]
        changes = line["changes"]
        print(
            f"[34m{repo:{repo_w}} [0;33m[[31m{changes:2}[33m]    [3;32m {branch:{branch_w}}[0m"
        )
