import os

from flask import Flask

from flask_container_scaffold.util import load_yaml


class AppScaffold(object):

    def __init__(self, app=None,
                 name=__name__, config=None):
        """
        This class provides a way to dynamically configure a Flask application.

        :param app: An existing Flask application, if passed, otherwise we will
                    create a new one
        :param name: The name of the application, defaults to __name__.
        :param config: A dict of configuration details. This can include
                       standard Flask configuration keys, like 'TESTING', or
                       custom keys (currently limited to a set list) to make
                       them available to the application during runtime

        """
        Flask.jinja_options = dict(Flask.jinja_options, trim_blocks=True,
                                   lstrip_blocks=True)
        self.app = app or Flask(name, instance_relative_config=True)
        self.config = config
        self._init_app()

    def _init_app(self):
        self._setup_instance_folder()
        self._configure_app()

    # NOTE: This method is old, and likely to go away, unless
    # we make it for dev mode only, as a production app should not
    # need to create folders.
    def _setup_instance_folder(self):
        # Ensure the instance folder exists
        try:
            os.makedirs(self.app.instance_path)
        except OSError:
            pass

    def _configure_app(self):
        if self.config is None:
            # load the instance config, if it exists
            self.app.config.from_pyfile('settings.cfg', silent=True)
        else:
            # load the config if passed in
            self.app.config.from_mapping(self.config)
            # Next, load from override file, if specified
        if os.environ.get('SETTINGS'):
            self.app.config.from_envvar('SETTINGS')
        # Next, load env vars directly, which will override
        # any previous settings.
        self.setup_core_config_from_env()
        # Loop again, making sure everything in env_list is set somehow
        # on the config object.
        self.setup_core_config_from_env(verify=True)
        # Load the defaults yaml file
        default_conf = (self.app.config.get('DEFAULTS_FILE') or False)
        if default_conf:
            self.app.config.update(
                {'default_params': load_yaml(default_conf)})

    def get_config_list(self):
        # TODO: pull this from a file or take list instead
        config_list = ['GIT_BASE_URL', 'DEFAULTS_FILE']
        return config_list

    def setup_core_config_from_env(self, verify=False):
        # loop through the list, setting each value from env if it exists
        for i in self.get_config_list():
            if os.environ.get(i):
                self.app.config[i] = os.environ.get(i)
            if verify and not self.app.config.get(i):
                raise ValueError(f"No {i} set for Flask application")
