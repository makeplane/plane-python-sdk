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
from pydantic import BaseModel, StrictBool, StrictStr, conint, constr
from plane.models.timezone_enum import TimezoneEnum

class PatchedProjectUpdateRequest(BaseModel):
    """
    Serializer for updating projects with enhanced state and estimation management.  Extends project creation with update-specific validations including default state assignment, estimation configuration, and project setting modifications.  # noqa: E501
    """
    name: Optional[constr(strict=True, max_length=255, min_length=1)] = None
    description: Optional[StrictStr] = None
    project_lead: Optional[StrictStr] = None
    default_assignee: Optional[StrictStr] = None
    identifier: Optional[constr(strict=True, max_length=12, min_length=1)] = None
    icon_prop: Optional[Any] = None
    emoji: Optional[constr(strict=True, max_length=255)] = None
    cover_image: Optional[StrictStr] = None
    module_view: Optional[StrictBool] = None
    cycle_view: Optional[StrictBool] = None
    issue_views_view: Optional[StrictBool] = None
    page_view: Optional[StrictBool] = None
    intake_view: Optional[StrictBool] = None
    guest_view_all_features: Optional[StrictBool] = None
    archive_in: Optional[conint(strict=True, le=12, ge=0)] = None
    close_in: Optional[conint(strict=True, le=12, ge=0)] = None
    timezone: Optional[TimezoneEnum] = None
    default_state: Optional[StrictStr] = None
    estimate: Optional[StrictStr] = None
    __properties = ["name", "description", "project_lead", "default_assignee", "identifier", "icon_prop", "emoji", "cover_image", "module_view", "cycle_view", "issue_views_view", "page_view", "intake_view", "guest_view_all_features", "archive_in", "close_in", "timezone", "default_state", "estimate"]

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
    def from_json(cls, json_str: str) -> PatchedProjectUpdateRequest:
        """Create an instance of PatchedProjectUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if project_lead (nullable) is None
        # and __fields_set__ contains the field
        if self.project_lead is None and "project_lead" in self.__fields_set__:
            _dict['project_lead'] = None

        # set to None if default_assignee (nullable) is None
        # and __fields_set__ contains the field
        if self.default_assignee is None and "default_assignee" in self.__fields_set__:
            _dict['default_assignee'] = None

        # set to None if icon_prop (nullable) is None
        # and __fields_set__ contains the field
        if self.icon_prop is None and "icon_prop" in self.__fields_set__:
            _dict['icon_prop'] = None

        # set to None if emoji (nullable) is None
        # and __fields_set__ contains the field
        if self.emoji is None and "emoji" in self.__fields_set__:
            _dict['emoji'] = None

        # set to None if cover_image (nullable) is None
        # and __fields_set__ contains the field
        if self.cover_image is None and "cover_image" in self.__fields_set__:
            _dict['cover_image'] = None

        # set to None if default_state (nullable) is None
        # and __fields_set__ contains the field
        if self.default_state is None and "default_state" in self.__fields_set__:
            _dict['default_state'] = None

        # set to None if estimate (nullable) is None
        # and __fields_set__ contains the field
        if self.estimate is None and "estimate" in self.__fields_set__:
            _dict['estimate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PatchedProjectUpdateRequest:
        """Create an instance of PatchedProjectUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedProjectUpdateRequest.parse_obj(obj)

        _obj = PatchedProjectUpdateRequest.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "project_lead": obj.get("project_lead"),
            "default_assignee": obj.get("default_assignee"),
            "identifier": obj.get("identifier"),
            "icon_prop": obj.get("icon_prop"),
            "emoji": obj.get("emoji"),
            "cover_image": obj.get("cover_image"),
            "module_view": obj.get("module_view"),
            "cycle_view": obj.get("cycle_view"),
            "issue_views_view": obj.get("issue_views_view"),
            "page_view": obj.get("page_view"),
            "intake_view": obj.get("intake_view"),
            "guest_view_all_features": obj.get("guest_view_all_features"),
            "archive_in": obj.get("archive_in"),
            "close_in": obj.get("close_in"),
            "timezone": obj.get("timezone"),
            "default_state": obj.get("default_state"),
            "estimate": obj.get("estimate")
        })
        return _obj


