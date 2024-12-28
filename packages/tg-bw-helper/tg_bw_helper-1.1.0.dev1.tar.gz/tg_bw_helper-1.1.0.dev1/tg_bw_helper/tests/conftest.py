import getpass
import os
import pathlib
import sys
from unittest.mock import patch

import pytest

from tg_bw_helper import __main__ as main


@pytest.fixture()
def fake_bw_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "fake-bw.py")


@pytest.fixture()
def fake_bw_path_failing_master_password():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "fake-bw-failing-master-password.py",
    )


@pytest.fixture()
def fake_bw_path_not_logged_in():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "fake-bw-not-logged-in.py")


@pytest.fixture()
def fake_bw_unknown_error():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), "fake-bw-unknown-error.py")


def _fake_getpass(*args, **kwargs):
    return "masterpassword"


@pytest.fixture()
def fake_getpass():
    return patch.object(getpass, "getpass", _fake_getpass)


def _fake_empty_getpass(*args, **kwargs):
    return ""


@pytest.fixture()
def fake_empty_getpass():
    return patch.object(getpass, "getpass", _fake_empty_getpass)


@pytest.fixture()
def fake_path_environment(fake_bw_path):
    environ = os.environ.copy()
    environ.update(
        {
            "PATH": ":".join(
                [
                    # Path to the scripts
                    str(pathlib.Path(fake_bw_path).parent.absolute()),
                    # Path to python, that is needed to run which and others
                    str(pathlib.Path(sys.executable).parent.absolute()),
                ]
            )
        }
    )
    return patch.object(
        os,
        "environ",
        environ,
    )


@pytest.fixture()
def fake_which():
    return patch.object(main, "WHICH_EXECUTABLE_NAME", "fake-which.py")
