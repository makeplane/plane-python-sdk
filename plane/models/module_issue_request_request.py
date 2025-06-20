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


from pydantic import BaseModel, Field, StrictStr, conlist

class ModuleIssueRequestRequest(BaseModel):
    """
    Serializer for bulk work item assignment to modules.  Validates work item ID lists for batch operations including module assignment and work item organization workflows.  # noqa: E501
    """
    issues: conlist(StrictStr) = Field(default=..., description="List of issue IDs to add to the module")
    __properties = ["issues"]

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
    def from_json(cls, json_str: str) -> ModuleIssueRequestRequest:
        """Create an instance of ModuleIssueRequestRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ModuleIssueRequestRequest:
        """Create an instance of ModuleIssueRequestRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ModuleIssueRequestRequest.parse_obj(obj)

        _obj = ModuleIssueRequestRequest.parse_obj({
            "issues": obj.get("issues")
        })
        return _obj


