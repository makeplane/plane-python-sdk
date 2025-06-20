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





class PriorityEnum(str, Enum):
    """
    * `urgent` - Urgent * `high` - High * `medium` - Medium * `low` - Low * `none` - None
    """

    """
    allowed enum values
    """
    URGENT = 'urgent'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    NONE = 'none'

    @classmethod
    def from_json(cls, json_str: str) -> PriorityEnum: # noqa: F821
        """Create an instance of PriorityEnum from a JSON string"""
        return PriorityEnum(json.loads(json_str))


