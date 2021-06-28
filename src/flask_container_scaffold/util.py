from toolchest.yaml import parse


# TODO: extract this method out to toolchest library.
def load_yaml(filename='config.yml', logger=None):
    """
    Convenience wrapper around toolchest.yaml::parse to allow you to parse a
    file by path+name

    :param filename: A yaml file to be parsed
    :param logger: Optional logger for potential errors
    :return: A dictionary formed out of the yaml data
    """
    config = {}
    with open(filename, 'r') as file_handle:
        config = parse(file_handle, logger=logger)
    return config
