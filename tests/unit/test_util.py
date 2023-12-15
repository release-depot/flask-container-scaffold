import configparser

import pytest

from flask_container_scaffold.base import BaseApiModel
from flask_container_scaffold.util import load_cfg, parse_input


def test_valid_cfg_file(mock_custom_only_extra_cfg):
    """
    GIVEN a valid cfg file
    WHEN we try to load it
    THEN we get back the expected python dict
    """
    expected = {'custom_section': {'Different_case': 'val',
                                   'all_lower': 'something'}}
    parsed = load_cfg(mock_custom_only_extra_cfg)
    assert parsed == expected


def test_invalid_cfg_file(mock_extra_settings_file):
    """
    GIVEN an invalid, Flask-style cfg file
    WHEN we try to load it
    THEN we get a MissingSectionHeaderError
    """
    with pytest.raises(configparser.MissingSectionHeaderError):
        load_cfg(mock_extra_settings_file)


class FakeApiModelExtension(BaseApiModel):
    code: int = 1


class FakeModel(FakeApiModelExtension):
    code: int = 0
    name: str


class TestParseInput:

    def test_no_data(self, app):
        """
        GIVEN a request with no parameters of any type
        WHEN we call parse_input on that request
        THEN we get a BaseApiModel returned with a code of 400
        AND an error explaining what is wrong
        """
        with app.test_request_context():
            retval = parse_input(app.logger, FakeModel)
            assert 'Field required' in retval.error
            assert isinstance(retval, BaseApiModel)

    def test_no_data_custom_return(self, app):
        """
        GIVEN a request with no parameters of any type
        WHEN we call parse_input on that request with a custom default_return
        THEN we get a custom object returned with additional fields
        AND an error explaining what is wrong
        """
        with app.test_request_context():
            retval = parse_input(app.logger, FakeModel, FakeApiModelExtension)
            assert retval.code == 1
            assert 'Field required' in retval.error
            assert isinstance(retval, BaseApiModel)

    @pytest.mark.parametrize("input_type,input_val",
                             [('json', {'name': 'foo'}),
                              ('qs', 'name=foo'),
                              ('form', {'name': 'foo'})])
    def test_parses_json(self, input_type, input_val, app):
        """
        GIVEN a request with json, a query string or form data
        WHEN we call parse_input on that request
        THEN we get a populated object returned, of the type requested.
        """
        context = {'json': app.test_request_context(json=input_val),
                   'qs': app.test_request_context(query_string=input_val),
                   'form': app.test_request_context(data=input_val)}
        with context.get(input_type):
            retval = parse_input(app.logger, FakeModel)
            assert retval.code == 0
            assert retval.error == ''
            assert retval.name == 'foo'
            assert isinstance(retval, FakeModel)
