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

from datetime import date, datetime
from typing import Any, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, constr
from plane.models.module_status_enum import ModuleStatusEnum

class Module(BaseModel):
    """
    Comprehensive module serializer with work item metrics and member management.  Provides complete module data including work item counts by status, member relationships, and progress tracking for feature-based project organization.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    total_issues: Optional[StrictInt] = None
    cancelled_issues: Optional[StrictInt] = None
    completed_issues: Optional[StrictInt] = None
    started_issues: Optional[StrictInt] = None
    unstarted_issues: Optional[StrictInt] = None
    backlog_issues: Optional[StrictInt] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    name: constr(strict=True, max_length=255) = Field(...)
    description: Optional[StrictStr] = None
    description_text: Optional[Any] = None
    description_html: Optional[Any] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    status: Optional[ModuleStatusEnum] = None
    view_props: Optional[Any] = None
    sort_order: Optional[Union[StrictFloat, StrictInt]] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    archived_at: Optional[datetime] = None
    logo_props: Optional[Any] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    lead: Optional[StrictStr] = None
    __properties = ["id", "total_issues", "cancelled_issues", "completed_issues", "started_issues", "unstarted_issues", "backlog_issues", "created_at", "updated_at", "deleted_at", "name", "description", "description_text", "description_html", "start_date", "target_date", "status", "view_props", "sort_order", "external_source", "external_id", "archived_at", "logo_props", "created_by", "updated_by", "project", "workspace", "lead"]

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
    def from_json(cls, json_str: str) -> Module:
        """Create an instance of Module from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "total_issues",
                            "cancelled_issues",
                            "completed_issues",
                            "started_issues",
                            "unstarted_issues",
                            "backlog_issues",
                            "created_at",
                            "updated_at",
                            "deleted_at",
                            "created_by",
                            "updated_by",
                            "project",
                            "workspace",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if description_text (nullable) is None
        # and __fields_set__ contains the field
        if self.description_text is None and "description_text" in self.__fields_set__:
            _dict['description_text'] = None

        # set to None if description_html (nullable) is None
        # and __fields_set__ contains the field
        if self.description_html is None and "description_html" in self.__fields_set__:
            _dict['description_html'] = None

        # set to None if start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.start_date is None and "start_date" in self.__fields_set__:
            _dict['start_date'] = None

        # set to None if target_date (nullable) is None
        # and __fields_set__ contains the field
        if self.target_date is None and "target_date" in self.__fields_set__:
            _dict['target_date'] = None

        # set to None if view_props (nullable) is None
        # and __fields_set__ contains the field
        if self.view_props is None and "view_props" in self.__fields_set__:
            _dict['view_props'] = None

        # set to None if external_source (nullable) is None
        # and __fields_set__ contains the field
        if self.external_source is None and "external_source" in self.__fields_set__:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and __fields_set__ contains the field
        if self.external_id is None and "external_id" in self.__fields_set__:
            _dict['external_id'] = None

        # set to None if archived_at (nullable) is None
        # and __fields_set__ contains the field
        if self.archived_at is None and "archived_at" in self.__fields_set__:
            _dict['archived_at'] = None

        # set to None if logo_props (nullable) is None
        # and __fields_set__ contains the field
        if self.logo_props is None and "logo_props" in self.__fields_set__:
            _dict['logo_props'] = None

        # set to None if created_by (nullable) is None
        # and __fields_set__ contains the field
        if self.created_by is None and "created_by" in self.__fields_set__:
            _dict['created_by'] = None

        # set to None if updated_by (nullable) is None
        # and __fields_set__ contains the field
        if self.updated_by is None and "updated_by" in self.__fields_set__:
            _dict['updated_by'] = None

        # set to None if lead (nullable) is None
        # and __fields_set__ contains the field
        if self.lead is None and "lead" in self.__fields_set__:
            _dict['lead'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Module:
        """Create an instance of Module from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Module.parse_obj(obj)

        _obj = Module.parse_obj({
            "id": obj.get("id"),
            "total_issues": obj.get("total_issues"),
            "cancelled_issues": obj.get("cancelled_issues"),
            "completed_issues": obj.get("completed_issues"),
            "started_issues": obj.get("started_issues"),
            "unstarted_issues": obj.get("unstarted_issues"),
            "backlog_issues": obj.get("backlog_issues"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "description_text": obj.get("description_text"),
            "description_html": obj.get("description_html"),
            "start_date": obj.get("start_date"),
            "target_date": obj.get("target_date"),
            "status": obj.get("status"),
            "view_props": obj.get("view_props"),
            "sort_order": obj.get("sort_order"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "archived_at": obj.get("archived_at"),
            "logo_props": obj.get("logo_props"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "lead": obj.get("lead")
        })
        return _obj


