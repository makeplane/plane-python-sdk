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

class IssueAttachmentUploadRequest(BaseModel):
    """
    Serializer for work item attachment upload request validation.  Handles file upload metadata validation including size, type, and external integration tracking for secure work item document attachment workflows.  # noqa: E501
    """
    name: constr(strict=True, min_length=1) = Field(default=..., description="Original filename of the asset")
    type: Optional[constr(strict=True, min_length=1)] = Field(default=None, description="MIME type of the file")
    size: StrictInt = Field(default=..., description="File size in bytes")
    external_id: Optional[constr(strict=True, min_length=1)] = Field(default=None, description="External identifier for the asset (for integration tracking)")
    external_source: Optional[constr(strict=True, min_length=1)] = Field(default=None, description="External source system (for integration tracking)")
    __properties = ["name", "type", "size", "external_id", "external_source"]

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
    def from_json(cls, json_str: str) -> IssueAttachmentUploadRequest:
        """Create an instance of IssueAttachmentUploadRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueAttachmentUploadRequest:
        """Create an instance of IssueAttachmentUploadRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueAttachmentUploadRequest.parse_obj(obj)

        _obj = IssueAttachmentUploadRequest.parse_obj({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "size": obj.get("size"),
            "external_id": obj.get("external_id"),
            "external_source": obj.get("external_source")
        })
        return _obj


