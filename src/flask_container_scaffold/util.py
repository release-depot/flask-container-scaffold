import configparser

from toolchest.yaml import parse


# TODO: extract this method out to toolchest library.
def load_yaml(filename='config.yml', logger=None):
    """
    Convenience wrapper around toolchest.yaml::parse to allow you to parse a
    file by path+name

    :param str filename: A yaml file to be parsed
    :param Logger logger: Optional logger for potential errors
    :return: A dictionary formed out of the yaml data
    """
    config = {}
    with open(filename, 'r') as file_handle:
        config = parse(file_handle, logger=logger)
    return config


def load_cfg(conf_file):
    """
    Load a cfg file

    :param str conf_file: A cfg/ini file to be parsed
    :return: A dictionary formed out of the cfg file data
    :raises: configparser.MissingSectionHeaderError, FileNotFoundError
    """
    config = configparser.ConfigParser()
    # The following setting tells the parser not to alter the keys it
    # has read in.  The default behavior converts these to lowercase:
    # https://docs.python.org/3/library/configparser.html#configparser.ConfigParser.optionxform
    config.optionxform = lambda option: option
    with open(conf_file) as conf:
        config.read_file(conf)
    return _parse_cfg(config)


def _parse_cfg(config):
    config_dict = {}
    for section in config.sections():
        settings_dict = {}
        for key in config[section]:
            settings_dict[key] = config[section][key]
        config_dict.update({section: settings_dict})
    return config_dict
