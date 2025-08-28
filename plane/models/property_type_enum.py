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


class PropertyTypeEnum(str, Enum):
    """
    * `TEXT` - Text * `DATETIME` - Datetime * `DECIMAL` - Decimal * `BOOLEAN` - Boolean * `OPTION` - Option * `RELATION` - Relation * `URL` - URL * `EMAIL` - Email * `FILE` - File
    """

    """
    allowed enum values
    """
    TEXT = 'TEXT'
    DATETIME = 'DATETIME'
    DECIMAL = 'DECIMAL'
    BOOLEAN = 'BOOLEAN'
    OPTION = 'OPTION'
    RELATION = 'RELATION'
    URL = 'URL'
    EMAIL = 'EMAIL'
    FILE = 'FILE'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of PropertyTypeEnum from a JSON string"""
        return cls(json.loads(json_str))


