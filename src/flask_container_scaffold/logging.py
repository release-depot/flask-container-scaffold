import logging

from flask import has_request_context

from flask_container_scaffold.network import get_remote_addr_from_flask


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
    def format(self, record):
        # If the record already has remote_addr, don't override it
        if hasattr(record, 'remote_addr') and record.remote_addr is not None:
            return super().format(record)

        if has_request_context():
            remote_addr = get_remote_addr_from_flask()
            record.remote_addr = remote_addr
        else:
            record.remote_addr = "-"

        return super().format(record)
