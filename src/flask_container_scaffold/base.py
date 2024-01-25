import warnings

from pydantic import BaseModel

"""
Common base class to allow us to have a common place to put errors and
messages. This class can be extended based on your use case if needed.
"""


class BaseApiModel(BaseModel):
    error: str = ''
    msg: str = ''

    def __init__(self, **data):
        warnings.warn("'BaseApiModel' is deprecated and should be changed to "
                      "'BaseApiView' before version 0.4.0", DeprecationWarning)
        super().__init__(**data)


class BaseApiView(BaseModel):
    errors: dict = {}
    msg: str = ''
