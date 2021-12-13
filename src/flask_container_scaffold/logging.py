import logging

from flask import has_request_context, request


class FlaskRequestFormatter(logging.Formatter):
    """
    A Formatter logging class to add IP information to the log records.

    Usage example::

      from flask_container_scaffold.logging import FlaskRequestFormatter

      dictConfig({
          'version': 1,
          'formatters': {
              'default': {
                  '()': FlaskRequestFormatter,
                  'format': '[%(asctime)s] %(remote_addr)s %(levelname)s: %(message)s',
              },
          },
          ...
      })
    """

    def get_ip_from_forwarded(self, field):
        # RFC 7239 defines the following format for the Forwarded field:
        # for=12.34.56.78;host=example.com;proto=https, for=23.45.67.89
        # In testing, the first IP has consistently been the real user IP.
        forwarded = field.split(",")[0]
        for value in forwarded.split(";"):
            if value.startswith("for="):
                return value.split("=")[1]
        else:
            return None

    def format(self, record):
        if has_request_context():
            # HTTP_FORWARDED seems to be the most reliable way to get the
            # user real IP.
            forwarded = request.environ.get('HTTP_FORWARDED')
            if forwarded:
                ip = self.get_ip_from_forwarded(forwarded)
                record.remote_addr = ip or request.remote_addr
            else:
                record.remote_addr = request.remote_addr
        else:
            record.remote_addr = "-"

        return super().format(record)
