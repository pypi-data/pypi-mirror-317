#!/usr/bin/env python3
# coding: utf-8
from __future__ import annotations

import os
import os.path
import shlex
import subprocess
import sys
from glob import glob
from typing import List, Iterable

from joker.filesys.dirs import DirectoryBoundToolkit


def printcmd(cmd: List[str], **kwargs):
    kwargs.setdefault("file", sys.stderr)
    print(*[shlex.quote(s) for s in cmd], **kwargs)


class Repository(DirectoryBoundToolkit):
    def __init__(self, path: str):
        dotgit_dir = os.path.join(path, ".git")
        if not os.path.isdir(dotgit_dir):
            raise NotADirectoryError(dotgit_dir)
        super().__init__(path)

    def under_dotgit_dir(self, *paths) -> str:
        return self.under(".git", *paths)

    @classmethod
    def find(cls, path: str) -> Iterable["Repository"]:
        pattern = os.path.join(path, "*", ".git")
        dotgit_paths = glob(pattern)
        for dotgit_path in dotgit_paths:
            try:
                yield cls(os.path.split(dotgit_path)[0])
            except NotADirectoryError:
                continue

    def pull(self):
        cmd = ["git", "pull"]
        printcmd(cmd)
        subprocess.run(cmd, cwd=self.base_dir, check=True)

    def check_command(self, cmd: list):
        sp = subprocess.run(cmd, cwd=self.base_dir, capture_output=True)
        return sp.stdout.decode("utf-8").strip()

    def get_current_branch(self) -> str:
        cmd = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        return self.check_command(cmd)

    def get_status_lines(self) -> list:
        cmd = ["git", "status", "--short"]
        return self.check_command(cmd).splitlines()

    def get_commit_info(self) -> dict:
        cmd = ["git", "log", "-1", "--pretty=%ae%n%h%n%ci%n%s"]
        keys = ["author", "commit", "committed_at", "message"]
        lines = self.check_command(cmd).splitlines()
        if len(lines) < len(keys):
            return {}
        info = dict(zip(keys, lines))
        info.update(
            {
                "branch": self.get_current_branch(),
                "status": self.get_status_lines(),
            }
        )
        return info

    def get_content(self, commit_id: str, path: str) -> bytes:
        """
        Args:
            commit_id: e.g. 6fd0789084610ab7f1d87681d9cc189ab15102b1
            path: relative path inside the git repository
        Returns:
            content of the file of the version
        """
        cmd = ["git", "show", f"{commit_id}:{path}"]
        sp = subprocess.run(cmd, capture_output=True, cwd=self.base_dir)
        return sp.stdout


__all__ = ["Repository"]
