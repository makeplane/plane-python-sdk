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



from pydantic import BaseModel, Field, constr

class IssueLinkCreateRequest(BaseModel):
    """
    Serializer for creating work item external links with validation.  Handles URL validation, format checking, and duplicate prevention for attaching external resources to work items.  # noqa: E501
    """
    url: constr(strict=True, min_length=1) = Field(...)
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
    def from_json(cls, json_str: str) -> IssueLinkCreateRequest:
        """Create an instance of IssueLinkCreateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueLinkCreateRequest:
        """Create an instance of IssueLinkCreateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueLinkCreateRequest.parse_obj(obj)

        _obj = IssueLinkCreateRequest.parse_obj({
            "url": obj.get("url")
        })
        return _obj


