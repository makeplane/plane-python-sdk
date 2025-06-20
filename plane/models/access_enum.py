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





class AccessEnum(str, Enum):
    """
    * `INTERNAL` - INTERNAL * `EXTERNAL` - EXTERNAL
    """

    """
    allowed enum values
    """
    INTERNAL = 'INTERNAL'
    EXTERNAL = 'EXTERNAL'

    @classmethod
    def from_json(cls, json_str: str) -> AccessEnum: # noqa: F821
        """Create an instance of AccessEnum from a JSON string"""
        return AccessEnum(json.loads(json_str))


