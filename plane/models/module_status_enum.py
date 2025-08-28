# coding: utf-8

"""
    The Plane REST API

    The Plane REST API  Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

    The version of the API Spec: 0.0.1
    Contact: support@plane.so
    This class is auto generated.

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


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
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ModuleStatusEnum from a JSON string"""
        return cls(json.loads(json_str))


