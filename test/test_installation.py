# This module is part of GitPython and is released under
# the BSD License: https://opensource.org/license/bsd-3-clause/

import ast
import os
import subprocess

from git.compat import is_win
from test.lib import TestBase, VirtualEnvironment, with_rw_directory


class TestInstallation(TestBase):
    @with_rw_directory
    def test_installation(self, rw_dir):
        venv = self._set_up_venv(rw_dir)
        result = subprocess.run(
            [venv.pip, "install", "."],
            stdout=subprocess.PIPE,
            cwd=venv.sources,
        )
        self.assertEqual(
            0,
            result.returncode,
            msg=result.stderr or result.stdout or "Can't install project",
        )
        result = subprocess.run([venv.python, "-c", "import git"], stdout=subprocess.PIPE, cwd=venv.sources)
        self.assertEqual(
            0,
            result.returncode,
            msg=result.stderr or result.stdout or "Selftest failed",
        )
        result = subprocess.run(
            [venv.python, "-c", "import sys;import git; print(sys.path)"],
            stdout=subprocess.PIPE,
            cwd=venv.sources,
        )
        syspath = result.stdout.decode("utf-8").splitlines()[0]
        syspath = ast.literal_eval(syspath)
        self.assertEqual(
            "",
            syspath[0],
            msg="Failed to follow the conventions for https://docs.python.org/3/library/sys.html#sys.path",
        )
        self.assertTrue(syspath[1].endswith("gitdb"), msg="Failed to add gitdb to sys.path")
        
    @staticmethod
    def _set_up_venv(rw_dir):
        venv = VirtualEnvironment(rw_dir, with_pip=True)
        os.symlink(
            os.path.dirname(os.path.dirname(__file__)),
            venv.sources,
            target_is_directory=True,
        )
        return venv
