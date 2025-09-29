# coding: utf-8

"""
    The Plane REST API

    The Plane REST API  Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

    The version of the API Spec: 0.0.2
    Contact: support@plane.so
    This class is auto generated.

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class IssueRelationCreateRelationTypeEnum(str, Enum):
    """
    * `blocking` - Blocking * `blocked_by` - Blocked By * `duplicate` - Duplicate * `relates_to` - Relates To * `start_before` - Start Before * `start_after` - Start After * `finish_before` - Finish Before * `finish_after` - Finish After
    """

    """
    allowed enum values
    """
    BLOCKING = 'blocking'
    BLOCKED_BY = 'blocked_by'
    DUPLICATE = 'duplicate'
    RELATES_TO = 'relates_to'
    START_BEFORE = 'start_before'
    START_AFTER = 'start_after'
    FINISH_BEFORE = 'finish_before'
    FINISH_AFTER = 'finish_after'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of IssueRelationCreateRelationTypeEnum from a JSON string"""
        return cls(json.loads(json_str))


