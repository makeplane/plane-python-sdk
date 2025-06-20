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
from pydantic import BaseModel, Field, StrictInt, constr
from plane.models.entity_type_enum import EntityTypeEnum
from plane.models.type_enum import TypeEnum

class UserAssetUploadRequest(BaseModel):
    """
    Serializer for user asset upload requests.  This serializer validates the metadata required to generate a presigned URL for uploading user profile assets (avatar or cover image) directly to S3 storage. Supports JPEG, PNG, WebP, JPG, and GIF image formats with size validation.  # noqa: E501
    """
    name: constr(strict=True, min_length=1) = Field(default=..., description="Original filename of the asset")
    type: Optional[TypeEnum] = Field(default=None, description="MIME type of the file  * `image/jpeg` - JPEG * `image/png` - PNG * `image/webp` - WebP * `image/jpg` - JPG * `image/gif` - GIF")
    size: StrictInt = Field(default=..., description="File size in bytes")
    entity_type: EntityTypeEnum = Field(default=..., description="Type of user asset  * `USER_AVATAR` - User Avatar * `USER_COVER` - User Cover")
    __properties = ["name", "type", "size", "entity_type"]

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
    def from_json(cls, json_str: str) -> UserAssetUploadRequest:
        """Create an instance of UserAssetUploadRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UserAssetUploadRequest:
        """Create an instance of UserAssetUploadRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UserAssetUploadRequest.parse_obj(obj)

        _obj = UserAssetUploadRequest.parse_obj({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "size": obj.get("size"),
            "entity_type": obj.get("entity_type")
        })
        return _obj


