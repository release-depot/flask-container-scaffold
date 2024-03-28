from celery import Celery

from flask_container_scaffold.base_scaffold import BaseScaffold


class CeleryScaffold(BaseScaffold):

    def __init__(self, flask_app=None, name=__name__, config=None,
                 settings_required=False,
                 instance_path=None,
                 instance_relative_config=True):
        """
        This class provides both a flask 'app' and a celery 'app' that has been
        configured via flask. All of the parameters are the same as BaseScaffold.
        Any naming changes are noted below.

        :param obj flask_app: An existing Flask application, if passed,
            otherwise we will create a new one using BaseScaffold. This is the same
            as the app parameter in BaseScaffold.
        """
        super().__init__(flask_app, name, config, settings_required,
                         instance_path, instance_relative_config)
        self.flask_app = flask_app or self.flask_app
        self.celery_app = Celery(self.flask_app.name)
        self.celery_app.config_from_object(self.flask_app.config.get("CELERY"))
        self.celery_app.set_default()
        # Add the celery app as an extension to the flask app so it can be easily
        # accessed if a flask application factory pattern is used.
        # see https://flask.palletsprojects.com/en/2.3.x/patterns/celery/ for details.
        self.flask_app.extensions["celery"] = self.celery_app
