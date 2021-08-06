import pytest
from flask_container_scaffold.app_scaffold import AppScaffold

# Tests with testing config true:


def test_config_valid_settings_file(mock_env_vars):
    """
    GIVEN a test mapping is passed to create_app
    AND a valid SETTINGS and DEFAULTS_FILE env var is set
    WHEN we try to create the app
    THEN it creates an instance of the app
    """
    app = AppScaffold(config={'TESTING': True}).app
    assert app is not None
    url = 'http://some.site/cgit/plain/additional-tags?h='
    assert app.config.get('GIT_BASE_URL') == url


def test_config_invalid_settings_file(monkeypatch):
    """
    GIVEN a test mapping is passed to create_app
    AND an invalid SETTINGS env var is set
    WHEN we try to create the app
    THEN it raises a FileNotFoundError
    """
    monkeypatch.setenv('SETTINGS', '/some/path/fake.cfg')
    with pytest.raises(FileNotFoundError):
        AppScaffold(config={'TESTING': True})


def test_hash_with_config(mock_defaults_file):
    """
    GIVEN a test mapping is passed to create_app
    AND it includes the required config values
    WHEN we try to create the app
    THEN it creates an instance of the app
    """
    url = 'http://foo.com/cgit'
    app = AppScaffold(config={
        'TESTING': True,
        'GIT_BASE_URL': url,
        'DEFAULTS_FILE': mock_defaults_file
    }).app
    assert app is not None
    assert app.config.get('GIT_BASE_URL') == url
    assert app.config.get('DEFAULTS_FILE') == mock_defaults_file


def test_hash_with_missing_config():
    """
    GIVEN a test mapping is passed to create_app
    AND it includes nothing else
    WHEN we try to create the app
    THEN it fails to start the app
    AND throws an error to indicate missing config
    """
    with pytest.raises(ValueError):
        AppScaffold(config={'TESTING': True})


def test_setting_env_vars_directly_only(mock_defaults_file, monkeypatch):
    """
    GIVEN a test mapping is passed to create_app
    AND the required config values are set as env vars
    WHEN we try to create the app
    THEN it creates an instance of the app
    """
    url = 'http://foo.com/cgit'
    monkeypatch.setenv('GIT_BASE_URL', url)
    monkeypatch.setenv('DEFAULTS_FILE', mock_defaults_file)
    app = AppScaffold(config={'TESTING': True}).app
    assert app is not None
    assert app.config.get('GIT_BASE_URL') == url
    assert app.config.get('DEFAULTS_FILE') == mock_defaults_file


def test_setting_incorrect_env_var(monkeypatch):
    """
    GIVEN a test mapping is passed to create_app
    AND the wrong config values are set as env vars
    WHEN we try to create the app
    THEN it fails to start the app
    AND throws an error
    """
    monkeypatch.setenv('WRONG_KEY', 'http://foo.com/cgit')
    with pytest.raises(ValueError):
        AppScaffold(config={'TESTING': True})
