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
from pydantic import BaseModel, StrictStr, constr
from plane.models.access_enum import AccessEnum

class IssueCommentCreateRequest(BaseModel):
    """
    Serializer for creating work item comments.  Handles comment creation with JSON and HTML content support, access control, and external integration tracking.  # noqa: E501
    """
    comment_json: Optional[Any] = None
    comment_html: Optional[StrictStr] = None
    access: Optional[AccessEnum] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    __properties = ["comment_json", "comment_html", "access", "external_source", "external_id"]

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
    def from_json(cls, json_str: str) -> IssueCommentCreateRequest:
        """Create an instance of IssueCommentCreateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if comment_json (nullable) is None
        # and __fields_set__ contains the field
        if self.comment_json is None and "comment_json" in self.__fields_set__:
            _dict['comment_json'] = None

        # set to None if external_source (nullable) is None
        # and __fields_set__ contains the field
        if self.external_source is None and "external_source" in self.__fields_set__:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and __fields_set__ contains the field
        if self.external_id is None and "external_id" in self.__fields_set__:
            _dict['external_id'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueCommentCreateRequest:
        """Create an instance of IssueCommentCreateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueCommentCreateRequest.parse_obj(obj)

        _obj = IssueCommentCreateRequest.parse_obj({
            "comment_json": obj.get("comment_json"),
            "comment_html": obj.get("comment_html"),
            "access": obj.get("access"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id")
        })
        return _obj


