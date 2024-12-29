"""Tests for pip-help package."""

import os
from subprocess import getstatusoutput

prg = "src/pip_help/main.py"
target_path = (os.path.join(os.path.expanduser("~"),  "pip_help_logs"))


def test_pip_help_exists():
    """Checks if the pip-help main file exists."""

    assert os.path.isfile(prg)


def test_usage():
    """Checks if the usage message is displayed."""

    for flag in ["-h", "--help"]:
        rv, out = getstatusoutput(f"python {prg} {flag}")
        assert rv == 0
        assert out.lower().startswith("usage")

def test_no_args():
    """Checks if the warning message is displayed when no arguments are provided."""

    rv, out = getstatusoutput(f"python {prg}")
    assert rv == 0
    assert out.lower().startswith("warning")


def test_dir_creation():
    """
    Checks if the directory is created.
    """

    rv, out = getstatusoutput(f"python {prg} --install requests")
    assert rv == 0
    assert os.path.isdir(target_path)


def test_dir_deletion():
    """
    Checks if the directory is deleted after uninstalling the last package installed by pip-help.
    """

    rv, out = getstatusoutput(f"python {prg} --remove requests")
    assert rv == 0
    assert not os.path.isdir(target_path)

    
