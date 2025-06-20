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


from typing import Any, Optional
from pydantic import BaseModel, Field

class PatchedAssetUpdateRequest(BaseModel):
    """
    Serializer for asset status updates after successful upload completion.  Handles post-upload asset metadata updates including attribute modifications and upload confirmation for S3-based file storage workflows.  # noqa: E501
    """
    attributes: Optional[Any] = Field(default=None, description="Additional attributes to update for the asset")
    __properties = ["attributes"]

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
    def from_json(cls, json_str: str) -> PatchedAssetUpdateRequest:
        """Create an instance of PatchedAssetUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if attributes (nullable) is None
        # and __fields_set__ contains the field
        if self.attributes is None and "attributes" in self.__fields_set__:
            _dict['attributes'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PatchedAssetUpdateRequest:
        """Create an instance of PatchedAssetUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedAssetUpdateRequest.parse_obj(obj)

        _obj = PatchedAssetUpdateRequest.parse_obj({
            "attributes": obj.get("attributes")
        })
        return _obj


