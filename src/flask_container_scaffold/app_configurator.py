from flask_container_scaffold.util import load_yaml, load_cfg


class AppConfigurator(object):

    def __init__(self, app, relative=True):
        """
        This class handles loading and parsing of custom configuration
        for your Flask app.

        :param obj app: An existing Flask application
        :param bool relative: Whether filenames found in configuration are
            assumed to be relative to instance path rather than application
            root.
        """
        self.app = app
        self.relative = relative

    def parse(self, custom):
        """
        Parse any custom configuration passed in for the app

        :param obj custom: A String or dictionary to parse and add to the
            application config.
        """
        if isinstance(custom, dict):
            for key in custom:
                self.parse(custom[key])
        else:
            self._parse_conf_item(custom)

    def _parse_conf_item(self, item):
        """
        Check if the config item is a string pointing to a file.
        If it is, and we support the filetype, call the appropriate
        function to add the contents of the file to app.config object
        """
        supported_extensions = ['cfg', 'yaml', 'yml']
        if isinstance(item, str):
            item_type = item.rsplit(".")[-1]
        else:
            item_type = 'not a file'
        # If this is a file reference, and we support the type,
        # detect the path, and the read the file and add the contents
        # to the app config.
        if item_type in supported_extensions:
            item = self._detect_path(item)
            self._add_to_config(item, item_type)
        return item

    def _detect_path(self, path):
        """
        When preparing to parse a file, determine if we have a explicit path
        or if we are looking in the instance folder.
        """
        if path.startswith('/'):
            pass
        else:
            if self.relative:
                path = self.app.instance_path + path.replace('instance', '')
            else:
                path = self.app.instance_path + path

        return path

    def _add_to_config(self, file, file_type):
        """
        Call the appropriate parser based on filetype
        """
        current_dict = {}
        if file_type in ['yaml', 'yml']:
            current_dict = load_yaml(file)
        elif file_type == 'cfg':
            current_dict = load_cfg(file)
        self.parse(current_dict)
        self.app.config.update(current_dict)
