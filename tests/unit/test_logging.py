from logging import LogRecord

from flask import Flask

from flask_container_scaffold.logging import FlaskRequestFormatter


FORMAT = "[%(remote_addr)s] %(msg)s"


def test_request_formatter_no_context():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called without a request context
    THEN the log message contains "-" instead of an IP
    """
    record = LogRecord('', 1, '', 1, 'Test message', '', None)

    formatter = FlaskRequestFormatter(FORMAT)

    assert formatter.format(record) == "[-] Test message"


def test_request_formatter_with_no_forwarded_ip():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called within a request context
    AND HTTP_FORWARDED isn't set
    THEN the log message contains the remote_addr IP
    """
    record = LogRecord('', 1, '', 1, 'Test message', '', None)

    with Flask("test").test_request_context(
            environ_base=(("REMOTE_ADDR", "1.2.3.4"),)):
        formatter = FlaskRequestFormatter(FORMAT)
        assert formatter.format(record) == "[1.2.3.4] Test message"


def test_request_formatter_with_forwarded_ip():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called within a request context
    AND HTTP_FORWARDED exists
    THEN the log message contains the forwarded IP
    """
    env = (("REMOTE_ADDR", "1.2.3.4"),
           ("HTTP_FORWARDED", "for=10.10.10.10;host=example.com;proto=http"),)
    record = LogRecord('', 1, '', 1, 'Test message', '', None)

    with Flask("test").test_request_context(environ_base=env):
        formatter = FlaskRequestFormatter(FORMAT)
        assert formatter.format(record) == "[10.10.10.10] Test message"


def test_request_formatter_with_several_forwarded_ips():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called within a request context
    AND HTTP_FORWARDED contains several IPs
    THEN the log message contains the first forwarded IP
    """
    env = (("REMOTE_ADDR", "1.2.3.4"),
           ("HTTP_FORWARDED", "for=10.10.10.10;host=example.com, for=1.1.1.1"))
    record = LogRecord('', 1, '', 1, 'Test message', '', None)

    with Flask("test").test_request_context(environ_base=env):
        formatter = FlaskRequestFormatter(FORMAT)
        assert formatter.format(record) == "[10.10.10.10] Test message"


def test_request_formatter_with_malformed_forwarded_field():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called within a request context
    AND HTTP_FORWARDED isn't the right format
    THEN the log message contains the remote address
    """
    env = (("REMOTE_ADDR", "1.2.3.4"),
           ("HTTP_FORWARDED", "host"),)
    record = LogRecord('', 1, '', 1, 'Test message', '', None)

    with Flask("test").test_request_context(environ_base=env):
        formatter = FlaskRequestFormatter(FORMAT)
        assert formatter.format(record) == "[1.2.3.4] Test message"


def test_request_formatter_with_remote_addr_already_set():
    """
    GIVEN a properly initialised FlaskRequestFormatter
    WHEN it is called with a record that already has remote_addr set
    THEN the log message contains that preset remote address
    """
    env = (("REMOTE_ADDR", "1.2.3.4"),
           ("HTTP_FORWARDED", "host"),)
    record = LogRecord('', 1, '', 1, 'Test message', '', None)
    record.remote_addr = '1.1.1.1'

    with Flask("test").test_request_context(environ_base=env):
        formatter = FlaskRequestFormatter(FORMAT)
        assert formatter.format(record) == "[1.1.1.1] Test message"
