import sys
from unittest.mock import patch

from tg_bw_helper import __main__ as main


def test_bw_does_not_exist(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            f"{fake_bw_path}--fake",
            "--vault-item",
            "item2",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == "masterpassword"
    assert "Max retries exceeded" not in captured.err


def test_bw_not_found_automatically(fake_getpass, fake_path_environment, fake_which, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--vault-item",
            "item2",
        ],
    ), fake_path_environment, fake_which, fake_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == "masterpassword"
    assert "Max retries exceeded" not in captured.err


def test_bw_empty_master_password(fake_bw_path_failing_master_password, fake_empty_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path_failing_master_password,
            "--vault-item",
            "item2",
        ],
    ), fake_empty_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == ""
    assert "Max retries exceeded" not in captured.err
    assert "Empty master password" in captured.err


def test_bw_master_password_fails(fake_bw_path_failing_master_password, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path_failing_master_password,
            "--vault-item",
            "item2",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == "masterpassword"
    assert "Max retries (3) exceeded" in captured.err


def test_bw_not_logged_in(fake_bw_path_not_logged_in, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path_not_logged_in,
            "--vault-item",
            "item2",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == "masterpassword"
    assert "Use `bw login`" in captured.err


def test_bw_unknown_error(fake_bw_unknown_error, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_unknown_error,
            "--vault-item",
            "item2",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    # This comes directly from user input, in our case from fake_getpass, which is used after master password fails
    # three times
    assert captured.out == "masterpassword"
