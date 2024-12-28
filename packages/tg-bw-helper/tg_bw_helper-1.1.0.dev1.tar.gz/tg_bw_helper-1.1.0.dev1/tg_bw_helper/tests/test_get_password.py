import pytest

import tg_bw_helper


def test_get_password(fake_bw_path):
    """Tests if password can be extracted from existing items"""
    assert tg_bw_helper.get_bw_pass(fake_bw_path, "item2", None, "SESSION_TOKEN") == "pass"
    assert tg_bw_helper.get_bw_pass(fake_bw_path, "item1", "Main ansible", "SESSION_TOKEN") == "pa$$word"


def test_get_missing_password(fake_bw_path):
    """Tests if missing item does not crash the script"""
    with pytest.raises(tg_bw_helper.BWFieldNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item1", None, "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWFieldNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item2", "Main ansible", "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWItemNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item3", "Main ansible", "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWFieldNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item1", "This field does not exist", "SESSION_TOKEN")


def test_get_malformed_item(fake_bw_path):
    """Tests if malformed item does not crash the script"""
    with pytest.raises(tg_bw_helper.BWItemNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item4", None, "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWItemNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item4", "Main ansible", "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWFieldNotFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item_bad", "Main ansible", "SESSION_TOKEN")


def test_get_multiple_items(fake_bw_path):
    """Tests if malformed item does not crash the script"""
    with pytest.raises(tg_bw_helper.BWMultipleItemsFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item", None, "SESSION_TOKEN")

    with pytest.raises(tg_bw_helper.BWMultipleItemsFound):
        tg_bw_helper.get_bw_pass(fake_bw_path, "item", "Main ansible", "SESSION_TOKEN")
