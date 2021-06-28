import os
import pytest


@pytest.fixture
def config_defaults():
    _dir = os.path.dirname(os.path.realpath(__file__))
    return _dir


@pytest.fixture
def mock_defaults_file(config_defaults):
    return os.path.join(config_defaults, 'data', 'config.yml')


@pytest.fixture
def mock_settings_file(config_defaults):
    return os.path.join(config_defaults, 'data', 'settings.cfg')


@pytest.fixture
def mock_env_vars(mock_settings_file, mock_defaults_file, monkeypatch):
    monkeypatch.setenv('SETTINGS', mock_settings_file)
    monkeypatch.setenv('DEFAULTS_FILE', mock_defaults_file)
