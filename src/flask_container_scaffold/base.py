from pydantic import BaseModel

"""
Common base class to allow us to have a common place to put errors and
messages. This class can be extended based on your use case if needed.
"""


class BaseApiModel(BaseModel):
    error: str = ''
    msg: str = ''
