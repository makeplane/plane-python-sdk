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





class RelationTypeEnum(str, Enum):
    """
    * `ISSUE` - Issue * `USER` - User
    """

    """
    allowed enum values
    """
    ISSUE = 'ISSUE'
    USER = 'USER'

    @classmethod
    def from_json(cls, json_str: str) -> RelationTypeEnum: # noqa: F821
        """Create an instance of RelationTypeEnum from a JSON string"""
        return RelationTypeEnum(json.loads(json_str))


