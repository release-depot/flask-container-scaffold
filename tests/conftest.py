import os
import pytest


@pytest.fixture
def config_defaults():
    _dir = os.path.dirname(os.path.realpath(__file__))
    return _dir


@pytest.fixture
def mock_custom_only_folder(config_defaults):
    return os.path.join(config_defaults, 'data', 'custom')


@pytest.fixture
def mock_custom_only_settings_file(mock_custom_only_folder):
    return os.path.join(mock_custom_only_folder, 'config.yml')


@pytest.fixture
def mock_custom_only_bad_file(mock_custom_only_folder):
    return os.path.join(mock_custom_only_folder, 'bad_config.yml')


@pytest.fixture
def mock_custom_only_extra_cfg(mock_custom_only_folder):
    return os.path.join(mock_custom_only_folder, 'extra.cfg')


@pytest.fixture
def mock_custom_only_cfg_w_includes(mock_custom_only_folder):
    return os.path.join(mock_custom_only_folder, 'has_includes.cfg')


@pytest.fixture
def mock_instance_folder(config_defaults):
    return os.path.join(config_defaults, 'data')


@pytest.fixture
def mock_flask_settings_file(config_defaults):
    return os.path.join(config_defaults, 'data', 'settings.cfg')


@pytest.fixture
def mock_extra_settings_file(config_defaults):
    return os.path.join(config_defaults, 'data', 'extra.cfg')


@pytest.fixture
def mock_custom_settings_file(config_defaults):
    return os.path.join(config_defaults, 'data', 'config.yml')


@pytest.fixture
def mock_env_vars(mock_flask_settings_file, monkeypatch):
    monkeypatch.setenv('FLASK_SETTINGS', mock_flask_settings_file)


@pytest.fixture
def mock_env_override_vars(mock_extra_settings_file, monkeypatch):
    monkeypatch.setenv('FLASK_SETTINGS', mock_extra_settings_file)
