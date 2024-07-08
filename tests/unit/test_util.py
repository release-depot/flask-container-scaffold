import configparser

import pytest

from flask_container_scaffold.base import BaseApiView
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


class FakeApiModelExtension(BaseApiView):
    code: int = 1


class FakeModel(FakeApiModelExtension):
    fake_id: int = 1
    code: int = 0
    name: str


class FakeModel2(FakeApiModelExtension):
    code: int = 0
    name: str
    status: str


class ComplexInput(FakeModel):
    field1: str
    field2: str


class TestParseInput:

    def test_no_data(self, app):
        """
        GIVEN a request with no parameters of any type
        WHEN we call parse_input on that request
        THEN we get a BaseApiView returned with a code of 400
        AND an error explaining what is wrong
        """
        with app.test_request_context():
            retval = parse_input(app.logger, FakeModel)
            assert (len(retval.errors)) == 1
            assert 'name' in retval.errors
            assert 'Field required' == retval.errors.get('name')
            assert isinstance(retval, BaseApiView)

    @pytest.mark.parametrize("to_parse,required_attrs",
                             [(FakeModel, ['name']),
                              (FakeModel2, ['name', 'status'])])
    def test_no_data_custom_return(self, to_parse, required_attrs, app):
        """
        GIVEN a request with no parameters of any type
        WHEN we call parse_input on that request with a custom default_return
        THEN we get a custom object returned with additional fields
        AND an error explaining what is wrong
        """
        with app.test_request_context():
            retval = parse_input(app.logger, to_parse, FakeApiModelExtension)
            assert retval.code == 1
            assert retval.msg == f"Errors detected: {len(required_attrs)}"
            for missing_attr in retval.errors:
                assert missing_attr in required_attrs
                assert retval.errors.get(missing_attr) == 'Field required'
            assert isinstance(retval, BaseApiView)

    @pytest.mark.parametrize("input_val",
                             [{'name': 'foo'},
                              {'name': 'foo', 'fake_id': 5}])
    def test_parses_url_params_json(self, input_val, app):
        """
        GIVEN a request with a url parameter (such as endpoint/<id>)
        WHEN we call parse_input on that request
        THEN we get a populated object returned with <id> properly set
        AND any json data appropriately parsed
        """
        with app.test_request_context('endpoint/2', json=input_val):
            retval = parse_input(app.logger, FakeModel)
            assert retval.fake_id == 2
            assert retval.code == 0
            assert retval.errors == {}
            assert retval.name == 'foo'
            assert isinstance(retval, FakeModel)

    @pytest.mark.parametrize("input_qs,input_form",
                             [('field1=foo&fake_id=8',
                               {'field2': 'foo', 'name': 'bob'}),
                              ('field1=foo&name=bob',
                               {'field2': 'foo', 'name': 'tim'}),
                              ('field1=foo&name=bob&field2=foo',
                               {})])
    def test_parses_url_params_non_json(self, input_qs, input_form, app):
        """"
        GIVEN a request with a url parameter (such as endpoint/<id>)
        WHEN we call parse_input on that request
        THEN we get a populated object returned with <id> properly set
        AND any query strings or forms appropriately parsed
        """

        with app.test_request_context('endpoint/2',
                                      query_string=input_qs, data=input_form):
            retval = parse_input(app.logger, ComplexInput)
            assert retval.fake_id == 2
            assert retval.code == 0
            assert retval.errors == {}
            assert retval.name == 'bob'
            assert isinstance(retval, ComplexInput)
