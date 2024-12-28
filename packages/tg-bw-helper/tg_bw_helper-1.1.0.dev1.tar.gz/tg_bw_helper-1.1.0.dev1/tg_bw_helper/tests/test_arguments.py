import sys
from unittest.mock import patch

from tg_bw_helper import __main__ as main


def test_vault_entry(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        ["__main__.py", "--bw-executable", fake_bw_path, "--vault-item", "item2"],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "pass"


def test_vault_entry_bw_found_automatically(fake_getpass, fake_path_environment, fake_which, capsys):
    with patch.object(
        sys,
        "argv",
        ["__main__.py", "--vault-item", "item2"],
    ), patch.object(main, "BASE_BW_EXECUTABLE_NAME", "fake-bw.py"), fake_path_environment, fake_which, fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "pass"


def test_vault_entry_is_not_existing(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        ["__main__.py", "--bw-executable", fake_bw_path, "--vault-item", "item3"],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "masterpassword"


def test_vault_entry_with_field(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path,
            "--vault-item",
            "item1",
            "--vault-item-field",
            "Legacy ansible",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "$ecure"


def test_vault_entry_with_wrong_field(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path,
            "--vault-item",
            "item1",
            "--vault-item-field",
            "Pizza delivery",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "masterpassword"


def test_vault_entry_with_too_broad_query(fake_bw_path, fake_getpass, capsys):
    with patch.object(
        sys,
        "argv",
        [
            "__main__.py",
            "--bw-executable",
            fake_bw_path,
            "--vault-item",
            "item",
        ],
    ), fake_getpass:
        main.run()

    captured = capsys.readouterr()
    assert captured.out == "masterpassword"
