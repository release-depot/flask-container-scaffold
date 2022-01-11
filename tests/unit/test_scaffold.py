import configparser

import pytest
from flask import Flask

from flask_container_scaffold.app_scaffold import AppScaffold

# Tests for base FLASK_SETTINGS


def test_no_config_valid_settings_file(mock_instance_folder):
    """
    GIVEN no config is passed into app_scaffold
    AND a valid settings.cfg file exists in the specified instance path
    WHEN we create the app
    THEN it creates an instance of the app
    AND sets any values in the settings file
    """
    scaffold = AppScaffold(instance_path=mock_instance_folder)
    url = 'http://some.site/cgit/plain/additional-tags?h='
    assert scaffold.app.config.get('GIT_BASE_URL') == url
    assert scaffold.app.config.get('CUSTOM_SETTINGS') == 'instance/config.yml'
    assert scaffold.app.config.get('RANDOM_VAL') == 'farkle'


def test_settings_required_no_config_no_settings_file_no_env_setting():
    """
    GIVEN no config is passed into app_scaffold
    AND no settings.cfg is in the expected location
    AND we have not set FLASK_SETTINGS
    AND settings_required=True
    WHEN we create the app
    THEN it raises a RuntimeError
    """
    with pytest.raises(RuntimeError):
        AppScaffold(settings_required=True)


def test_no_config_no_settings_file_no_env_setting():
    """
    GIVEN no config is passed into app_scaffold
    AND no settings.cfg is in the expected location
    AND we have not set FLASK_SETTINGS
    AND we have left the default of settings_required=False
    WHEN we create the app
    THEN it creates the app with default settings.
    """
    app = AppScaffold()
    assert app is not None


def test_no_config_valid_settings_file_env_override(mock_instance_folder,
                                                    mock_env_override_vars):
    """
    GIVEN no config is passed into app_scaffold
    AND a valid settings.cfg file exists in the specified instance path
    AND FLASK_SETTINGS points to a config file
    WHEN we create the app
    THEN it creates an instance of the app
    AND sets any values in the settings file,
    AND overrides existing values with those in the FLASK_SETTINGS file
    """
    scaffold = AppScaffold(instance_path=mock_instance_folder)
    url = 'http://some.site/cgit/plain/additional-tags?h='
    assert scaffold.app.config.get('GIT_BASE_URL') == url
    assert scaffold.app.config.get('CUSTOM_SETTINGS') == 'instance/config.yml'
    assert scaffold.app.config.get('RANDOM_VAL') == 'baz'
    assert scaffold.app.config.get('ANOTHER_VALUE') == 'I am so extra'


def test_no_config_no_settings_file_valid_env_override(mock_env_vars,
                                                       mock_instance_folder):
    """
    GIVEN no config is passed into app_scaffold
    AND no settings.cfg is found
    AND FLASK_SETTINGS points to a config file
    WHEN we create the app
    THEN it creates an instance of the app
    AND sets any values in the FLASK_SETTINGS settings file
    """
    scaffold = AppScaffold(instance_path=mock_instance_folder)
    url = 'http://some.site/cgit/plain/additional-tags?h='
    assert scaffold.app.config.get('GIT_BASE_URL') == url
    assert scaffold.app.config.get('RANDOM_VAL') == 'farkle'


def test_config_valid_settings_file(mock_instance_folder):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND a valid settings.cfg is found
    WHEN we try to create the app
    THEN it creates an instance of the app
    """
    scaffold = AppScaffold(config={'TESTING': True},
                           instance_path=mock_instance_folder,
                           settings_required=True)
    url = 'http://some.site/cgit/plain/additional-tags?h='
    assert scaffold.app.config.get('GIT_BASE_URL') == url


def test_config_invalid_settings_file(monkeypatch):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND an invalid file is referenced by the FLASK_SETTINGS env var
    WHEN we try to create the app
    THEN it raises a FileNotFoundError
    """
    monkeypatch.setenv('FLASK_SETTINGS', '/some/path/fake.cfg')
    with pytest.raises(FileNotFoundError):
        AppScaffold(config={'TESTING': True})


# Tests for CUSTOM SETTINGS

def test_hash_with_config(mock_custom_only_settings_file,
                          mock_custom_only_folder):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND it includes the required config values
    WHEN we try to create the app
    THEN it creates an instance of the app
    """
    url = 'http://foo.com/cgit'
    config = {'TESTING': True,
              'CUSTOM_SETTINGS':
              {'GIT_BASE_URL': url,
               'DEFAULTS_FILE': mock_custom_only_settings_file}}
    scaffold = AppScaffold(config=config,
                           instance_path=mock_custom_only_folder)
    assert scaffold.app is not None
    custom_base = scaffold.app.config.get('CUSTOM_SETTINGS')
    assert custom_base.get('GIT_BASE_URL') == url
    assert custom_base.get('DEFAULTS_FILE') == mock_custom_only_settings_file
    assert (scaffold.app.config.get('default_params').get('a_key') ==
            'another value')
    assert (scaffold.app.config.get('extra_config').get('important_stuff') ==
            'abc')


def test_hash_with_missing_config():
    """
    GIVEN a config mapping is passed to AppScaffold
    AND it includes nothing else
    AND settings_required=True
    WHEN we try to create the app
    THEN it fails to start the app
    AND throws an error to indicate missing config
    """
    with pytest.raises(RuntimeError):
        AppScaffold(config={'TESTING': True},
                    settings_required=True)


def test_setting_env_vars_directly_only(mock_custom_settings_file,
                                        mock_flask_settings_file,
                                        mock_instance_folder,
                                        monkeypatch):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND the required config values are set as env vars
    WHEN we try to create the app
    THEN it creates an instance of the app with the expected setting
    """
    url = 'http://some.site/cgit/plain/additional-tags?h='
    monkeypatch.setenv('FLASK_SETTINGS', mock_flask_settings_file)
    monkeypatch.setenv('CUSTOM_SETTINGS', mock_custom_settings_file)
    scaffold = AppScaffold(config={'TESTING': True},
                           instance_path=mock_instance_folder)
    assert scaffold.app is not None
    assert scaffold.app.config.get('GIT_BASE_URL') == url
    assert (scaffold.app.config.get('CUSTOM_SETTINGS') ==
            'instance/config.yml')
    assert (scaffold.app.config.get('default_params').get('a_key') ==
            'some value')
    assert scaffold.app.config.get('default_params').get('key_two') == 3
    assert (scaffold.app.config.get('default_params').get('a_list') ==
            ['list value'])


def test_valid_instance_configs(mock_instance_folder):
    """
    GIVEN an existing Flask app
    WHEN it is passed into the Scaffold
    THEN the default settings in the specified instance folder are loaded
    """
    url = 'http://some.site/cgit/plain/additional-tags?h='
    base_app = Flask('TestApp', instance_path=mock_instance_folder,
                     instance_relative_config=True)
    scaffold = AppScaffold(app=base_app)
    assert scaffold.app is not None
    assert scaffold.app.config.get('GIT_BASE_URL') == url
    assert (scaffold.app.config.get('CUSTOM_SETTINGS') ==
            'instance/config.yml')
    assert (scaffold.app.config.get('default_params').get('a_key') ==
            'some value')


def test_loads_all_values_in_extra_cfg_file(mock_custom_only_extra_cfg):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND that mapping contains a custom setting pointing to a cfg file
    WHEN we try to create the app
    THEN it creates an instance of the app with the expected setting
    """
    scaffold = AppScaffold(config={
        'TESTING': True,
        'CUSTOM_SETTINGS': mock_custom_only_extra_cfg})
    assert scaffold.app is not None
    base_custom = scaffold.app.config.get('custom_section')
    assert base_custom.get('Different_case') == 'val'
    assert base_custom.get('all_lower') == 'something'


def test_fails_on_bad_custom_cfg_format(mock_extra_settings_file):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND that mapping contains a custom setting pointing to an invalid cfg file
    WHEN we try to create the app
    THEN it raises a MissingSectionHeaderError
    """
    with pytest.raises(configparser.MissingSectionHeaderError):
        AppScaffold(config={
            'TESTING': True,
            'CUSTOM_SETTINGS': mock_extra_settings_file})


def test_referenced_config_file_not_found(mock_custom_only_bad_file):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND an invalid file is referenced by the FLASK_SETTINGS env var
    WHEN we try to create the app
    THEN it raises a FileNotFoundError
    """
    with pytest.raises(FileNotFoundError):
        AppScaffold(config={
            'TESTING': True,
            'CUSTOM_SETTINGS': mock_custom_only_bad_file})


def test_recursively_adds_config(mock_custom_only_cfg_w_includes,
                                 mock_custom_only_folder):
    """
    GIVEN a config mapping is passed to AppScaffold
    AND it includes a cfg file that in turn references another config file
    WHEN we try to create the app
    THEN it creates an instance of the app
    AND sets values from both config files as expected
    """
    config = {'CUSTOM_SETTINGS': mock_custom_only_cfg_w_includes}
    scaffold = AppScaffold(config=config,
                           instance_path=mock_custom_only_folder)
    assert scaffold.app is not None
    # Check custom sections in cfg file were added:
    assert (scaffold.app.config.get('my_config').get('one_key') ==
            'foo')
    assert (scaffold.app.config.get('my_config').get('two_key') ==
            'bar')
    # Check items in file referenced by first config were loaded:
    assert (scaffold.app.config.get('default_params').get('a_key') ==
            'another value')
    assert (scaffold.app.config.get('extra_config').get('important_stuff') ==
            'abc')
    # Check that we do NOT have the path to the nested config file added
    # to app.config
    assert 'more_yaml' not in scaffold.app.config
