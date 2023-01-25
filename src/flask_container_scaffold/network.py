from flask import request


def get_ip_from_forwarded_field(field):
    # RFC 7239 defines the following format for the Forwarded field:
    # for=12.34.56.78;host=example.com;proto=https, for=23.45.67.89
    # In testing, the first IP has consistently been the real user IP.
    forwarded = field.split(",")[0]
    for value in forwarded.split(";"):
        if value.startswith("for="):
            return value.split("=")[1]
    else:
        return None


def get_remote_addr_from_flask():
    # HTTP_FORWARDED seems to be the most reliable way to get the
    # user real IP.
    forwarded = request.environ.get('HTTP_FORWARDED')
    if forwarded:
        ip = get_ip_from_forwarded_field(forwarded)
        return ip or request.remote_addr
    else:
        return request.remote_addr
