import configparser

import pytest

from flask_container_scaffold.util import load_cfg


def test_valid_cfg_file(mock_custom_only_extra_cfg):
    """
    GIVEN a valid cfg file
    WHEN we try to load it
    THEN we get back the expected python dict
    """
    expected = {'custom_section': {'Different_case': 'val',
                                   'all_lower': 'something'}}
    parsed = load_cfg(mock_custom_only_extra_cfg)
    assert parsed == expected


def test_invalid_cfg_file(mock_extra_settings_file):
    """
    GIVEN an invalid, Flask-style cfg file
    WHEN we try to load it
    THEN we get a MissingSectionHeaderError
    """
    with pytest.raises(configparser.MissingSectionHeaderError):
        load_cfg(mock_extra_settings_file)
