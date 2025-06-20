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
from pydantic import BaseModel, Field, StrictStr, constr
from plane.models.intake_work_item_status_enum import IntakeWorkItemStatusEnum
from plane.models.issue_for_intake_request import IssueForIntakeRequest

class IntakeIssueCreateRequest(BaseModel):
    """
    Serializer for creating intake work items with embedded issue data.  Manages intake work item creation including nested issue creation, status assignment, and source tracking for issue queue management.  # noqa: E501
    """
    issue: IssueForIntakeRequest = Field(default=..., description="Issue data for the intake issue")
    intake: StrictStr = Field(...)
    status: Optional[IntakeWorkItemStatusEnum] = None
    snoozed_till: Optional[datetime] = None
    duplicate_to: Optional[StrictStr] = None
    source: Optional[constr(strict=True, max_length=255)] = None
    source_email: Optional[StrictStr] = None
    __properties = ["issue", "intake", "status", "snoozed_till", "duplicate_to", "source", "source_email"]

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
    def from_json(cls, json_str: str) -> IntakeIssueCreateRequest:
        """Create an instance of IntakeIssueCreateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of issue
        if self.issue:
            _dict['issue'] = self.issue.to_dict()
        # set to None if snoozed_till (nullable) is None
        # and __fields_set__ contains the field
        if self.snoozed_till is None and "snoozed_till" in self.__fields_set__:
            _dict['snoozed_till'] = None

        # set to None if duplicate_to (nullable) is None
        # and __fields_set__ contains the field
        if self.duplicate_to is None and "duplicate_to" in self.__fields_set__:
            _dict['duplicate_to'] = None

        # set to None if source (nullable) is None
        # and __fields_set__ contains the field
        if self.source is None and "source" in self.__fields_set__:
            _dict['source'] = None

        # set to None if source_email (nullable) is None
        # and __fields_set__ contains the field
        if self.source_email is None and "source_email" in self.__fields_set__:
            _dict['source_email'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IntakeIssueCreateRequest:
        """Create an instance of IntakeIssueCreateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IntakeIssueCreateRequest.parse_obj(obj)

        _obj = IntakeIssueCreateRequest.parse_obj({
            "issue": IssueForIntakeRequest.from_dict(obj.get("issue")) if obj.get("issue") is not None else None,
            "intake": obj.get("intake"),
            "status": obj.get("status"),
            "snoozed_till": obj.get("snoozed_till"),
            "duplicate_to": obj.get("duplicate_to"),
            "source": obj.get("source"),
            "source_email": obj.get("source_email")
        })
        return _obj


