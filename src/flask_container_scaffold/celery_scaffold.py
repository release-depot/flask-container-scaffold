from celery import Celery

from flask_container_scaffold.base_scaffold import BaseScaffold


class CeleryScaffold(BaseScaffold):

    def __init__(self, flask_app=None, name=__name__, config=None,
                 settings_required=False,
                 instance_path=None,
                 instance_relative_config=True):
        """
        This class provides both a flask 'app' and a celery 'app' that has been
        configured via flask.

        :param obj flask_app: An existing Flask application, if passed,
            otherwise we will create a new one using BaseScaffold.
        :param str name: The name of the application, defaults to __name__.
        :param dict config: A dict of configuration details. This can include
            standard Flask configuration keys, like 'TESTING', or
            'CUSTOM_SETTINGS' (which can be a string referencing a file with
            custom configuration, or a dictionary containing any values your
            application may need) to make them available to the application
            during runtime
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
        super().__init__(flask_app, name, config, settings_required,
                         instance_path, instance_relative_config)
        self.flask_app = flask_app or self.flask_app
        self.celery_app = Celery(self.flask_app.name)
        self.celery_app.config_from_object(self.flask_app.config.get("CELERY"))
        self.celery_app.set_default()
