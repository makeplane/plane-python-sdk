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





class IntakeWorkItemStatusEnum(int, Enum):
    """
    * `-2` - Pending * `-1` - Rejected * `0` - Snoozed * `1` - Accepted * `2` - Duplicate
    """

    """
    allowed enum values
    """
    NUMBER_MINUS_2 = -2
    NUMBER_MINUS_1 = -1
    NUMBER_0 = 0
    NUMBER_1 = 1
    NUMBER_2 = 2

    @classmethod
    def from_json(cls, json_str: str) -> IntakeWorkItemStatusEnum: # noqa: F821
        """Create an instance of IntakeWorkItemStatusEnum from a JSON string"""
        return IntakeWorkItemStatusEnum(json.loads(json_str))


