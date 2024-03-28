from flask_container_scaffold.base_scaffold import BaseScaffold


class AppScaffold(BaseScaffold):

    def __init__(self, app=None,
                 name=__name__, config=None,
                 settings_required=False,
                 instance_path=None,
                 instance_relative_config=True):
        """
        This class provides compatibility with versions of scaffold that
        expect an instance with an 'app' attribute. All of the parameters are
        the same as BaseScaffold and are passed directly through unmodified.
        """
        super().__init__(app, name, config, settings_required,
                         instance_path, instance_relative_config)
        self.app = app or self.flask_app
