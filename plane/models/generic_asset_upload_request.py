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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Set
from typing_extensions import Self

class GenericAssetUploadRequest(BaseModel):
    """
    Serializer for generic asset upload requests with project association.  Validates metadata for generating presigned URLs for workspace assets including project association, external system tracking, and file validation for document management and content storage workflows.
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)] = Field(description="Original filename of the asset")
    type: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="MIME type of the file")
    size: StrictInt = Field(description="File size in bytes")
    project_id: Optional[StrictStr] = Field(default=None, description="UUID of the project to associate with the asset")
    external_id: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="External identifier for the asset (for integration tracking)")
    external_source: Optional[Annotated[str, Field(min_length=1, strict=True)]] = Field(default=None, description="External source system (for integration tracking)")
    __properties: ClassVar[List[str]] = ["name", "type", "size", "project_id", "external_id", "external_source"]

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
        """Create an instance of GenericAssetUploadRequest from a JSON string"""
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
        """Create an instance of GenericAssetUploadRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "size": obj.get("size"),
            "project_id": obj.get("project_id"),
            "external_id": obj.get("external_id"),
            "external_source": obj.get("external_source")
        })
        return _obj


