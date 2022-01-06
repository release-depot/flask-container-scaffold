## flask-container-scaffold

[![pypi](https://img.shields.io/pypi/v/flask-container-scaffold.svg)](https://pypi.python.org/pypi/flask-container-scaffold)
[![tests](https://github.com/release-depot/flask-container-scaffold/actions/workflows/test.yml/badge.svg)](https://github.com/release-depot/flask-container-scaffold/actions/workflows/test.yml)
[![documentation](https://readthedocs.org/projects/flask-container-scaffold/badge/?version=latest)](https://flask-container-scaffold.readthedocs.io/en/latest/?badge=latest)

A common base layer for Flask applications that are deployed in containers.

This project is still in a very early stage, being pulled out from a flask-
based ReST service that was developed to be deployed in a container.  The
main issue it was created to solve was adding easy and consistent support
for flexible configuration.  For instance, in a development environment, there
may be a configuration file that is used, but in a container, you may need to
specify an environment variable that points to a yaml/json file, or some
filesystem mount that is very different from development.  Externalizing this
configuration allows for more flexibility in multiple environments.

## Installation

flask-container-scaffold can be installed via pip with:

    pip install flask-container-scaffold

## Usage

The library is meant to be used to do the basic configuration of a flask
application, and allows for the user to then do any further setup required once
the configuration is in place.  It is called from within your app factory
function like this:

    app = AppScaffold(name=__name__, config=config).app
    app.register_blueprint(foo.bp) # or whatever else you still need to do

The library supports two levels of configuration.

### Level 1: Flask Settings

The first is the standard flask configuration that can be used by default, but
with a bit of extra structure.  You can specify this configuration using any or
all of the following options:

1. Pass in the Flask config to AppScaffold via the config parameter (this is a
   dictionary).
2. Via a standard flask settings.cfg file.  Flask will look for this in the
   instance folder, which you can specify via the instance_path parameter to
   AppScaffold if it is not in the default location ('instance' within the app).
3. Via a FLASK_SETTINGS environment variable whose value is a path to a valid
   Flask settings.cfg file. This can be a relative path if the instance_config
   folder is specified, or can be an absolute path in all cases.

Note that Flask requires all config settings to be in CAPS, otherwise they will
not be included in the app.config dictionary on initialization.

AppScaffold will look for each of the items above, and they will be set in the
same order, if found.  So, for example, if you set:

    config= {'FOO': 'bar'}

when you call AppScaffold, but then have:

    FOO='something else'

in your file specified by the FLASK_SETTINGS environment variable, the latter
will overwrite the former.

### Level 2: Custom Settings

Custom settings are meant to be more flexible than the Flask settings, and can
be in whatever structure makes sense for your application.  These settings are
found and loaded by AppScaffold when you reference a Flask setting of
CUSTOM_SETTINGS in any of the following ways:

1. As a key in your config dict passed into AppScaffold
2. As a key in your settings.cfg file
3. As an environment variable whose value is a path to a valid file containing
   your custom configuration. This can be a relative path if the
   instance_config folder is specified, or can be an absolute path in all cases.

Currently, settings can be configured via a standard cfg file (using
[ini-file](https://docs.python.org/3/library/configparser.html#supported-ini-file-structure)
format) or a yaml file (which can end with '.yml' or '.yaml'). These files, in
turn, can reference additional files if needed.  Sections and structures are
supported, so long as they can be put into a python dictionary, and will be
added as-is, without additional formatting of case (which the python
ConfigParser library does by default). Also, keys can be in whatever case suits
your needs, which is a difference from the core Flask settings.

### Logger Formatting

After the application is initialized, the custom formatter can be
configured at any point in the code before logging is called. As an
example:

    from logging.config import dictConfig

    from flask_container_scaffold.logging import FlaskRequestFormatter

    dictConfig({
        'version': 1,
        'formatters': {
            'default': {
                '()': FlaskRequestFormatter,
                'format': '[%(asctime)s] %(remote_addr)s '
                '%(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': '/var/log/myapp.log',
                'backupCount': 3,
                'maxBytes': 15728640,  # 1024 * 1024 * 15
                'formatter': 'default',
            },
        },
        'loggers': {
            'main': {
                'level': 'INFO',
            },
        },
        'root': {
            'level': 'WARNING',
            'handlers': ['wsgi', 'file'],
        },
    })

## Development

### Setting up a development environment

You may set up your environment with virtualenv or another preferred tool for
managing virtual environments, but here are some directions for doing so using
[pipenv](https://pipenv.pypa.io/en/latest/). First, install pipenv:

    pip install --user pipenv

Next, using it to set up your development environment:

    pipenv update -d

If you prefer to use pip directly in your venv, specify the following
requirements files:

  - requirements.txt
  - test-requirements.txt

There is also a dist-requirements.txt, if you will be building the project
for distribution.

Any remaining directions will assume you are in your venv, which for pipenv,
can be activated like this:

    pipenv shell

Alternatively, any commands can be run in your pipenv venv by prepending with:

    pipenv run

This project attempts to follow most of the suggestions in the [python packaging
docs](https://packaging.python.org/tutorials/packaging-projects/) while also
supporting an easy to set up development environment.

### Building the project

If you wish to build the project for distribution:

    python -m build

