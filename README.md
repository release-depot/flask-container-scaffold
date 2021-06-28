# flask-container-scaffold

A common base layer for Flask applications that are deployed in containers.

This project is still in a very early stage, being pulled out from a flask-
based ReST service that was developed to be deployed in a container.  The
main issue it was created to solve was adding easy and consistent support
for flexible configuration.  For instance, in a development environment, there
may be a configuration file that is used, but in a container, you may need to
specify an environment variable that points to a yaml/json file, or some
filesystem mount that is very different from development.  Externalizing this
configuration allows for more flexibility in multiple environments.

### Installation

flask-container-scaffold can be installed via pip with:

    pip install flask-container-scaffold

### Usage

The library is meant to be used to do the basic configuration of a flask
application, and allows for the user to then do any further setup required once
the configuration is in place.  It is called from within your app factory
function like this:

    app = AppScaffold(name=__name__, test_config=test_config).app
    app.register_blueprint(foo.bp) # or whatever else you still need to do

The library currently has some hard-coded assumptions based on the project it
was originally used in, which will become more flexible over time.  The first is
that there is either a settings.cfg file in the standard flask instance folder,
or that there is a SETTINGS environment variable that points to a valid cfg
file.  The values currently supported in this file are GIT_BASE_URL and
DEFAULTS_FILE.  This is something that will be enhanced very soon, but is what
the original application used. The next assumption is that DEFAULTS_FILE is
specified in settings.cfg, or as an environment variable.  This file is already
completely flexible, and can contain any additional configuration your
application may need.  It is assumed this is a yaml file.  The contents of
the file are parsed and stored in app.config.default_params.

### Development

#### Setting up a development environment

You may set up your environment with virtualenv or another preferred tool for
managing virtual environments, but here are some directions for doing so using
[pipenv](https://pipenv.pypa.io/en/latest/). First, install pipenv:

    pip install --user pipenv

Next, using it to set up your development environment:

    pipenv update -d

If you prefer to use pip directly in your venv, simply specify the
requirements.txt and test-requirements.txt files.  There is also a
dist-requirements.txt, if you will be building the project for distribution.

Any remaining directions will assume you are in your venv, which for pipenv,
can be activated like this:

    pipenv shell

Alternatively, any commands can be run in your pipenv venv by prepending with:

    pipenv run

This project attempts to follow most of the suggestions in the [python packaging
docs](https://packaging.python.org/tutorials/packaging-projects/) while also
supporting an easy to set up development environment.

#### Building the project

If you wish to build the project for distribution:

    python -m build

