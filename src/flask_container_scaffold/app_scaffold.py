import os

from flask import Flask

from flask_container_scaffold.app_configurator import AppConfigurator


class AppScaffold(object):

    def __init__(self, app=None,
                 name=__name__, config=None,
                 settings_required=False,
                 instance_path=None,
                 instance_relative_config=True):
        """
        This class provides a way to dynamically configure a Flask application.

        :param obj app: An existing Flask application, if passed, otherwise we
            will create a new one
        :param str name: The name of the application, defaults to __name__.
        :param dict config: A dict of configuration details. This can include
            standard Flask configuration keys, like 'TESTING', or
            'CUSTOM_SETTINGS' (which can be a string referencing a file with custom
            configuration, or a dictionary containing any values your application
            may need) to make them available to the application during runtime
        :param bool settings_required: Whether your app requires certain
            settings be specified in a settings.cfg file
        :param str instance_path: Passthrough parameter to flask. An
            alternative instance path for the application. By default
            the folder 'instance' next to the package or module is
            assumed to be the instance path.
        :param bool instance_relative_config: Passthrough parameter to flask.
            If set to True relative filenames for loading the config
            are assumed to be relative to the instance path instead of
            the application root.

        """
        # TODO: Consider taking **kwargs here, so we can automatically support
        # all params the flask object takes, and just pass them through.  Keep
        # the ones we already have, as they are needed for the current code to
        # work.
        Flask.jinja_options = dict(Flask.jinja_options, trim_blocks=True,
                                   lstrip_blocks=True)
        self.app = (app or
                    Flask(name,
                          instance_relative_config=instance_relative_config,
                          instance_path=instance_path))
        self.config = config
        self.silent = not settings_required
        self.relative = instance_relative_config
        self._init_app()

    def _init_app(self):
        self._load_flask_settings()
        self._load_custom_settings()

    def _load_flask_settings(self):
        """
        This loads the 'core' settings, ie, anything you could set directly
        on a Flask app. These can be specified in the following order, each
        overriding the last, if specified:
        - via config mapping
        - via Flask settings.cfg file
        - via environment variable 'FLASK_SETTINGS'
        """
        config_not_loaded = True
        if self.config is not None:
            # load the config if passed in
            self.app.config.from_mapping(self.config)
            config_not_loaded = False
        # load the instance config, if it exists and/or is required
        try:
            self.app.config.from_pyfile('settings.cfg', silent=self.silent)
            config_not_loaded = False
        except Exception:
            config_not_loaded = True
        # Load any additional config specified in the FLASK_SETTINGS file,
        # if it exists. We only want to fail in the case where settings are
        # required by the app.
        if ((config_not_loaded and not self.silent) or
                os.environ.get('FLASK_SETTINGS')):
            self.app.config.from_envvar('FLASK_SETTINGS')

    def _load_custom_settings(self):
        """
        Load any custom configuration for the app from:
        - app.config['CUSTOM_SETTINGS']
        - environment variable 'CUSTOM_SETTINGS'
        """
        configurator = AppConfigurator(self.app, self.relative)
        if self.app.config.get('CUSTOM_SETTINGS') is not None:
            # load the config if passed in
            custom = self.app.config.get('CUSTOM_SETTINGS')
            configurator.parse(custom)
        # Next, load from override file, if specified
        if os.environ.get('CUSTOM_SETTINGS') is not None:
            custom = os.environ.get('CUSTOM_SETTINGS')
            configurator.parse(custom)
