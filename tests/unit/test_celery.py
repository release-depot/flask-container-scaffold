import pytest

from celery import Celery
from flask import Flask

from flask_container_scaffold.celery_scaffold import CeleryScaffold


def test_celery_flask_empty_config():
    """
    GIVEN an instance of CeleryScaffold with an empty config
    WHEN we try to create the app
    THEN we get a celery app and a flask app
    """
    scaffold = CeleryScaffold()
    assert scaffold.flask_app is not None
    assert isinstance(scaffold.flask_app, Flask)
    assert scaffold.celery_app is not None
    assert isinstance(scaffold.celery_app, Celery)


def test_flask_extension():
    """
    Given an instance of CeleryScaffold
    WHEN the apps are created
    THEN the flask extension has a celery element
    AND the celery app matches the flask extension
    """
    scaffold = CeleryScaffold()
    assert scaffold.flask_app is not None
    assert scaffold.celery_app is not None
    assert scaffold.flask_app.extensions.get("celery") is not None
    assert scaffold.celery_app == scaffold.flask_app.extensions["celery"]


def test_celery_broker_set():
    """
    GIVEN an instance of CeleryScaffold
    AND a config with a broker url
    WHEN we create the app
    THEN we get a celery app with a broker url matching the config
    """
    config = {'CELERY': {'broker': 'pyamqp://'}}
    scaffold = CeleryScaffold(config=config)
    app = scaffold.celery_app
    assert app is not None
    assert isinstance(app, Celery)
    assert config['CELERY']['broker'] == app.conf.find_value_for_key('broker')


def test_celery_bad_config():
    """
    GIVEN an instance of CeleryScaffold
    AND a config with a bad config item
    WHEN we create the app
    THEN we get a celery app
    AND the config doesn't have the bad item
    """
    config = {'CELERY': {'bad_config_item': 'my_bad_config'}}
    scaffold = CeleryScaffold(config=config)
    app = scaffold.celery_app
    assert app is not None
    assert isinstance(app, Celery)
    with pytest.raises(KeyError):
        app.conf.find_value_for_key('bad_config_item')
