# coding: utf-8

"""
Mercurial-related tasks.
"""

__all__ = ["BundleMercurialRepository"]


import os
import threading
import subprocess
from abc import abstractmethod

import luigi

from law.task.base import Task
from law.target.file import get_path
from law.target.local import LocalFileTarget
from law.parameter import NO_STR, CSVParameter
from law.decorator import log
from law.util import rel_path, interruptable_popen, quote_cmd


class BundleMercurialRepository(Task):

    task_namespace = "law.mercurial"

    exclude_files = CSVParameter(
        default=(),
        description="patterns of files to exclude, default: ()",
    )
    include_files = CSVParameter(
        default=(),
        description="patterns of files to force-include, takes precedence over .hgignore, "
        "default: ()",
    )
    custom_checksum = luigi.Parameter(
        default=NO_STR,
        description="a custom checksum to use, default: NO_STR",
    )

    def __init__(self, *args, **kwargs):
        super(BundleMercurialRepository, self).__init__(*args, **kwargs)

        self._checksum = None
        self._checksum_lock = threading.RLock(())

    @abstractmethod
    def get_repo_path(self):
        return

    @property
    def checksum(self):
        if self.custom_checksum != NO_STR:
            return self.custom_checksum

        with self._checksum_lock:
            if self._checksum is None:
                cmd = quote_cmd([
                    rel_path(__file__, "scripts", "repository_checksum.sh"),
                    get_path(self.get_repo_path()),
                ])

                code, out, _ = interruptable_popen(
                    cmd,
                    shell=True,
                    executable="/bin/bash",
                    stdout=subprocess.PIPE,
                )
                if code != 0:
                    raise Exception("repository checksum calculation failed")

                self._checksum = out.strip()

        return self._checksum

    def output(self):
        repo_base = os.path.basename(get_path(self.get_repo_path()))
        repo_base = os.path.abspath(os.path.expandvars(os.path.expanduser(repo_base)))
        return LocalFileTarget("{}_{}.tgz".format(repo_base, self.checksum))

    @log
    def run(self):
        with self.output().localize("w") as tmp:
            self.bundle(tmp.path)

    def bundle(self, dst_path):
        bundle_script = rel_path(__file__, "scripts", "bundle_repository.sh")
        cmd = [bundle_script, get_path(self.get_repo_path()), get_path(dst_path)]
        cmd += [" ".join(self.exclude_files)]
        cmd += [" ".join(self.include_files)]

        code = interruptable_popen(cmd, executable="/bin/bash")[0]
        if code != 0:
            raise Exception("repository bundling failed")
