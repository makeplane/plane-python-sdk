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
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr, constr

class LabelLite(BaseModel):
    """
    Lightweight label serializer for minimal data transfer.  Provides essential label information with visual properties, optimized for UI display and performance-critical operations.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    name: constr(strict=True, max_length=255) = Field(...)
    color: Optional[constr(strict=True, max_length=255)] = None
    __properties = ["id", "name", "color"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LabelLite:
        """Create an instance of LabelLite from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LabelLite:
        """Create an instance of LabelLite from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LabelLite.parse_obj(obj)

        _obj = LabelLite.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "color": obj.get("color")
        })
        return _obj


