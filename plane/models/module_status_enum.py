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





class ModuleStatusEnum(str, Enum):
    """
    * `backlog` - Backlog * `planned` - Planned * `in-progress` - In Progress * `paused` - Paused * `completed` - Completed * `cancelled` - Cancelled
    """

    """
    allowed enum values
    """
    BACKLOG = 'backlog'
    PLANNED = 'planned'
    IN_MINUS_PROGRESS = 'in-progress'
    PAUSED = 'paused'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

    @classmethod
    def from_json(cls, json_str: str) -> ModuleStatusEnum: # noqa: F821
        """Create an instance of ModuleStatusEnum from a JSON string"""
        return ModuleStatusEnum(json.loads(json_str))


