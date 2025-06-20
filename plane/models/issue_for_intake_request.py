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
from pydantic import BaseModel, Field, StrictStr, constr
from plane.models.priority_enum import PriorityEnum

class IssueForIntakeRequest(BaseModel):
    """
    Serializer for work item data within intake submissions.  Handles essential work item fields for intake processing including content validation and priority assignment for triage workflows.  # noqa: E501
    """
    name: constr(strict=True, max_length=255, min_length=1) = Field(...)
    description: Optional[Any] = None
    description_html: Optional[StrictStr] = None
    priority: Optional[PriorityEnum] = None
    __properties = ["name", "description", "description_html", "priority"]

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
    def from_json(cls, json_str: str) -> IssueForIntakeRequest:
        """Create an instance of IssueForIntakeRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueForIntakeRequest:
        """Create an instance of IssueForIntakeRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueForIntakeRequest.parse_obj(obj)

        _obj = IssueForIntakeRequest.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "description_html": obj.get("description_html"),
            "priority": obj.get("priority")
        })
        return _obj


