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
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, conlist, constr

class IssueActivity(BaseModel):
    """
    Serializer for work item activity and change history.  Tracks and represents work item modifications, state changes, and user interactions for audit trails and activity feeds.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    verb: Optional[constr(strict=True, max_length=255)] = None
    field: Optional[constr(strict=True, max_length=255)] = None
    old_value: Optional[StrictStr] = None
    new_value: Optional[StrictStr] = None
    comment: Optional[StrictStr] = None
    attachments: Optional[conlist(constr(strict=True, max_length=200), max_items=10)] = None
    old_identifier: Optional[StrictStr] = None
    new_identifier: Optional[StrictStr] = None
    epoch: Optional[Union[StrictFloat, StrictInt]] = None
    project: StrictStr = Field(...)
    workspace: StrictStr = Field(...)
    issue: Optional[StrictStr] = None
    issue_comment: Optional[StrictStr] = None
    actor: Optional[StrictStr] = None
    __properties = ["id", "created_at", "updated_at", "deleted_at", "verb", "field", "old_value", "new_value", "comment", "attachments", "old_identifier", "new_identifier", "epoch", "project", "workspace", "issue", "issue_comment", "actor"]

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
    def from_json(cls, json_str: str) -> IssueActivity:
        """Create an instance of IssueActivity from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "created_at",
                            "updated_at",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if field (nullable) is None
        # and __fields_set__ contains the field
        if self.field is None and "field" in self.__fields_set__:
            _dict['field'] = None

        # set to None if old_value (nullable) is None
        # and __fields_set__ contains the field
        if self.old_value is None and "old_value" in self.__fields_set__:
            _dict['old_value'] = None

        # set to None if new_value (nullable) is None
        # and __fields_set__ contains the field
        if self.new_value is None and "new_value" in self.__fields_set__:
            _dict['new_value'] = None

        # set to None if old_identifier (nullable) is None
        # and __fields_set__ contains the field
        if self.old_identifier is None and "old_identifier" in self.__fields_set__:
            _dict['old_identifier'] = None

        # set to None if new_identifier (nullable) is None
        # and __fields_set__ contains the field
        if self.new_identifier is None and "new_identifier" in self.__fields_set__:
            _dict['new_identifier'] = None

        # set to None if epoch (nullable) is None
        # and __fields_set__ contains the field
        if self.epoch is None and "epoch" in self.__fields_set__:
            _dict['epoch'] = None

        # set to None if issue (nullable) is None
        # and __fields_set__ contains the field
        if self.issue is None and "issue" in self.__fields_set__:
            _dict['issue'] = None

        # set to None if issue_comment (nullable) is None
        # and __fields_set__ contains the field
        if self.issue_comment is None and "issue_comment" in self.__fields_set__:
            _dict['issue_comment'] = None

        # set to None if actor (nullable) is None
        # and __fields_set__ contains the field
        if self.actor is None and "actor" in self.__fields_set__:
            _dict['actor'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueActivity:
        """Create an instance of IssueActivity from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueActivity.parse_obj(obj)

        _obj = IssueActivity.parse_obj({
            "id": obj.get("id"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "verb": obj.get("verb"),
            "field": obj.get("field"),
            "old_value": obj.get("old_value"),
            "new_value": obj.get("new_value"),
            "comment": obj.get("comment"),
            "attachments": obj.get("attachments"),
            "old_identifier": obj.get("old_identifier"),
            "new_identifier": obj.get("new_identifier"),
            "epoch": obj.get("epoch"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "issue": obj.get("issue"),
            "issue_comment": obj.get("issue_comment"),
            "actor": obj.get("actor")
        })
        return _obj


