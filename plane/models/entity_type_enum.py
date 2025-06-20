# coding: utf-8

"""
    The Plane REST API

    The Plane REST API  Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

    The version of the API Spec: 0.0.1
    Contact: support@plane.so
    This class is auto generated.

    Do not edit the class manually.
"""  # noqa: E501


import json
import re  # noqa: F401
from aenum import Enum





class EntityTypeEnum(str, Enum):
    """
    * `USER_AVATAR` - User Avatar * `USER_COVER` - User Cover
    """

    """
    allowed enum values
    """
    USER_AVATAR = 'USER_AVATAR'
    USER_COVER = 'USER_COVER'

    @classmethod
    def from_json(cls, json_str: str) -> EntityTypeEnum: # noqa: F821
        """Create an instance of EntityTypeEnum from a JSON string"""
        return EntityTypeEnum(json.loads(json_str))


