import configparser
import json

from flask import request
from pydantic import ValidationError
from toolchest.yaml import parse

from flask_container_scaffold.base import BaseApiModel


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


def parse_input(logger, obj, default_return=BaseApiModel):
    """
    Parses incoming request, returns a serializable object to return
    to the client in all cases. When there is a failure, the
    object contains error information.
    :param Logger logger: Instantiated logger object
    :param BaseModel obj: An object type based on a pydantic BaseModel to
                          attempt to parse.
    :param BaseApiModel default_return: An object type that will be returned if
                                        validation of obj fails. This object
                                        must descend from BaseApiModel or
                                        implement an error field of type str.
    :returns: Instantiated object of type obj on success, or default_return
              on failure to parse.
    """
    try:
        if request.is_json:
            parsed_args = obj.model_validate_json(json.dumps(request.json))
        else:
            if request.args:
                args = request.args
            else:
                args = request.form
            parsed_args = obj.model_validate_json(json.dumps(args.to_dict()))
    except ValidationError as e:
        logger.error(f"Validation error is: {e}")
        parsed_args = default_return(error=str(e.errors()[0]))
    return parsed_args
