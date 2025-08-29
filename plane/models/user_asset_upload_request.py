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

from pydantic import BaseModel, ConfigDict, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from plane.models.entity_type_enum import EntityTypeEnum
from plane.models.type_enum import TypeEnum
from typing import Set
from typing_extensions import Self

class UserAssetUploadRequest(BaseModel):
    """
    Serializer for user asset upload requests.  This serializer validates the metadata required to generate a presigned URL for uploading user profile assets (avatar or cover image) directly to S3 storage. Supports JPEG, PNG, WebP, JPG, and GIF image formats with size validation.
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)] = Field(description="Original filename of the asset")
    type: Optional[TypeEnum] = Field(default=None, description="MIME type of the file  * `image/jpeg` - JPEG * `image/png` - PNG * `image/webp` - WebP * `image/jpg` - JPG * `image/gif` - GIF")
    size: StrictInt = Field(description="File size in bytes")
    entity_type: EntityTypeEnum = Field(description="Type of user asset  * `USER_AVATAR` - User Avatar * `USER_COVER` - User Cover")
    __properties: ClassVar[List[str]] = ["name", "type", "size", "entity_type"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of UserAssetUploadRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserAssetUploadRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "size": obj.get("size"),
            "entity_type": obj.get("entity_type")
        })
        return _obj


