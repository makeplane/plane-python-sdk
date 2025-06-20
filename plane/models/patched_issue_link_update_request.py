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
from pydantic import BaseModel, constr

class PatchedIssueLinkUpdateRequest(BaseModel):
    """
    Serializer for updating work item external links.  Extends link creation with update-specific validation to prevent URL conflicts and maintain link integrity during modifications.  # noqa: E501
    """
    url: Optional[constr(strict=True, min_length=1)] = None
    __properties = ["url"]

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
    def from_json(cls, json_str: str) -> PatchedIssueLinkUpdateRequest:
        """Create an instance of PatchedIssueLinkUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PatchedIssueLinkUpdateRequest:
        """Create an instance of PatchedIssueLinkUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedIssueLinkUpdateRequest.parse_obj(obj)

        _obj = PatchedIssueLinkUpdateRequest.parse_obj({
            "url": obj.get("url")
        })
        return _obj


