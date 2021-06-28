# flask-container-scaffold
Common base layer for Flask applications that are deployed in containers.

## TEST

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

