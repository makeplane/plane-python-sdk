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

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, StrictBool, StrictStr, conlist, constr
from plane.models.access_enum import AccessEnum

class IssueComment(BaseModel):
    """
    Full serializer for work item comments with membership context.  Provides complete comment data including member status, content formatting, and edit tracking for collaborative work item discussions.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    is_member: Optional[StrictBool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    comment_stripped: Optional[StrictStr] = None
    comment_html: Optional[StrictStr] = None
    attachments: Optional[conlist(constr(strict=True, max_length=200), max_items=10)] = None
    access: Optional[AccessEnum] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    edited_at: Optional[datetime] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    issue: Optional[StrictStr] = None
    actor: Optional[StrictStr] = None
    __properties = ["id", "is_member", "created_at", "updated_at", "deleted_at", "comment_stripped", "comment_html", "attachments", "access", "external_source", "external_id", "edited_at", "created_by", "updated_by", "project", "workspace", "issue", "actor"]

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
    def from_json(cls, json_str: str) -> IssueComment:
        """Create an instance of IssueComment from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "is_member",
                            "created_at",
                            "updated_at",
                            "created_by",
                            "updated_by",
                            "project",
                            "workspace",
                            "issue",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if external_source (nullable) is None
        # and __fields_set__ contains the field
        if self.external_source is None and "external_source" in self.__fields_set__:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and __fields_set__ contains the field
        if self.external_id is None and "external_id" in self.__fields_set__:
            _dict['external_id'] = None

        # set to None if edited_at (nullable) is None
        # and __fields_set__ contains the field
        if self.edited_at is None and "edited_at" in self.__fields_set__:
            _dict['edited_at'] = None

        # set to None if created_by (nullable) is None
        # and __fields_set__ contains the field
        if self.created_by is None and "created_by" in self.__fields_set__:
            _dict['created_by'] = None

        # set to None if updated_by (nullable) is None
        # and __fields_set__ contains the field
        if self.updated_by is None and "updated_by" in self.__fields_set__:
            _dict['updated_by'] = None

        # set to None if actor (nullable) is None
        # and __fields_set__ contains the field
        if self.actor is None and "actor" in self.__fields_set__:
            _dict['actor'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueComment:
        """Create an instance of IssueComment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueComment.parse_obj(obj)

        _obj = IssueComment.parse_obj({
            "id": obj.get("id"),
            "is_member": obj.get("is_member"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "comment_stripped": obj.get("comment_stripped"),
            "comment_html": obj.get("comment_html"),
            "attachments": obj.get("attachments"),
            "access": obj.get("access"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "edited_at": obj.get("edited_at"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "issue": obj.get("issue"),
            "actor": obj.get("actor")
        })
        return _obj


