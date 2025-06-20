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
from pydantic import BaseModel, Field, StrictBool

class PatchedGenericAssetUpdateRequest(BaseModel):
    """
    Serializer for generic asset upload confirmation and status management.  Handles post-upload status updates for workspace assets including upload completion marking and metadata finalization.  # noqa: E501
    """
    is_uploaded: Optional[StrictBool] = Field(default=True, description="Whether the asset has been successfully uploaded")
    __properties = ["is_uploaded"]

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
    def from_json(cls, json_str: str) -> PatchedGenericAssetUpdateRequest:
        """Create an instance of PatchedGenericAssetUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PatchedGenericAssetUpdateRequest:
        """Create an instance of PatchedGenericAssetUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedGenericAssetUpdateRequest.parse_obj(obj)

        _obj = PatchedGenericAssetUpdateRequest.parse_obj({
            "is_uploaded": obj.get("is_uploaded") if obj.get("is_uploaded") is not None else True
        })
        return _obj


