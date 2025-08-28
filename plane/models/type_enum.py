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


class TypeEnum(str, Enum):
    """
    * `image/jpeg` - JPEG * `image/png` - PNG * `image/webp` - WebP * `image/jpg` - JPG * `image/gif` - GIF
    """

    """
    allowed enum values
    """
    IMAGE_SLASH_JPEG = 'image/jpeg'
    IMAGE_SLASH_PNG = 'image/png'
    IMAGE_SLASH_WEBP = 'image/webp'
    IMAGE_SLASH_JPG = 'image/jpg'
    IMAGE_SLASH_GIF = 'image/gif'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of TypeEnum from a JSON string"""
        return cls(json.loads(json_str))


