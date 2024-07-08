import configparser

from flask import request
from pydantic import ValidationError
from toolchest.yaml import parse

from flask_container_scaffold.base import BaseApiView


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


def parse_input(logger, obj, default_return=BaseApiView):
    """
    Parses incoming request, returns a serializable object to return
    to the client in all cases. When there is a failure, the
    object contains error information.

    :param Logger logger: Instantiated logger object
    :param BaseModel obj: An object type based on a pydantic BaseModel to
                          attempt to parse.
    :param BaseApiView default_return: An object type that will be returned if
                                       validation of obj fails. This object
                                       must descend from BaseApiView or
                                       implement an errors field of type dict.
    :returns: Instantiated object of type obj on success, or default_return
              on failure to parse.
    """
    args_dict = _preprocess_request()
    try:
        # Unpack the dict into keyword arguments
        parsed_args = obj(**args_dict)
    except ValidationError as e:
        logger.error(f"Validation error is: {e}")
        errors_result = {}
        errors_message = f"Errors detected: {len(e.errors())}"
        for error in e.errors():
            errors_result[error.get("loc")[0]] = error.get("msg")
        parsed_args = default_return(msg=errors_message, errors=errors_result)
    return parsed_args


def _preprocess_request() -> dict:
    """
    Checks the various places in a request that could contain parameters, and
    extracts them into a dictionary that can then be used for further parsing.
    This dictionary should contain no duplicates, and chooses what to use based
    on the following rules:

    1. If a request contains both parameters embedded in the url (like
    endpoint/1) AND
      * json data, they will be preferred in this order:
        - url-embedded
        - json data
      * query string and/or form data, they will be preferred in this order:
        - url-embedded
        - query string
        - form data
    2. If a request contains both json data AND either query strings or form
    data, only the json will be parsed. However, Flask currently prevents this
    from happening, as it will not allow a user to pass both types of data at
    the same time. The `curl` command is similarly mutually exclusive.

    :returns: dict containing the parsed parameters
    """
    processed_request = {}
    # Check for URL Parameters
    if request.view_args:
        processed_request = request.view_args
    # If the request has json input, parse that and combine with URL
    # parameters, preferring the latter.
    if request.is_json:
        processed_request = {**request.json, **processed_request}
    else:
        # Check in query-string for additional parameters. Prefer any that were
        # previously found in URL parameters.
        if request.args:
            processed_request = {**request.args.to_dict(), **processed_request}
        # Check in form for additional parameters. Prefer any that were previously
        # found in URL parameters or query-string.
        if request.form:
            processed_request = {**request.form.to_dict(), **processed_request}
    return processed_request
