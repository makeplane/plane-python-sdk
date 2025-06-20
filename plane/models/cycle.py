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
from typing import Any, Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr, conint, constr
from plane.models.timezone_enum import TimezoneEnum

class Cycle(BaseModel):
    """
    Cycle serializer with comprehensive project metrics and time tracking.  Provides cycle details including work item counts by status, progress estimates, and time-bound iteration data for project management and sprint planning.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    total_issues: Optional[StrictInt] = None
    cancelled_issues: Optional[StrictInt] = None
    completed_issues: Optional[StrictInt] = None
    started_issues: Optional[StrictInt] = None
    unstarted_issues: Optional[StrictInt] = None
    backlog_issues: Optional[StrictInt] = None
    total_estimates: Optional[Union[StrictFloat, StrictInt]] = None
    completed_estimates: Optional[Union[StrictFloat, StrictInt]] = None
    started_estimates: Optional[Union[StrictFloat, StrictInt]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    name: constr(strict=True, max_length=255) = Field(...)
    description: Optional[StrictStr] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    view_props: Optional[Any] = None
    sort_order: Optional[Union[StrictFloat, StrictInt]] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    progress_snapshot: Optional[Any] = None
    archived_at: Optional[datetime] = None
    logo_props: Optional[Any] = None
    timezone: Optional[TimezoneEnum] = None
    version: Optional[conint(strict=True, le=2147483647, ge=-2147483648)] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    owned_by: Optional[StrictStr] = None
    __properties = ["id", "total_issues", "cancelled_issues", "completed_issues", "started_issues", "unstarted_issues", "backlog_issues", "total_estimates", "completed_estimates", "started_estimates", "created_at", "updated_at", "deleted_at", "name", "description", "start_date", "end_date", "view_props", "sort_order", "external_source", "external_id", "progress_snapshot", "archived_at", "logo_props", "timezone", "version", "created_by", "updated_by", "project", "workspace", "owned_by"]

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
    def from_json(cls, json_str: str) -> Cycle:
        """Create an instance of Cycle from a JSON string"""
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
                            "total_estimates",
                            "completed_estimates",
                            "started_estimates",
                            "created_at",
                            "updated_at",
                            "deleted_at",
                            "created_by",
                            "updated_by",
                            "project",
                            "workspace",
                            "owned_by",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.start_date is None and "start_date" in self.__fields_set__:
            _dict['start_date'] = None

        # set to None if end_date (nullable) is None
        # and __fields_set__ contains the field
        if self.end_date is None and "end_date" in self.__fields_set__:
            _dict['end_date'] = None

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

        # set to None if progress_snapshot (nullable) is None
        # and __fields_set__ contains the field
        if self.progress_snapshot is None and "progress_snapshot" in self.__fields_set__:
            _dict['progress_snapshot'] = None

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

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Cycle:
        """Create an instance of Cycle from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Cycle.parse_obj(obj)

        _obj = Cycle.parse_obj({
            "id": obj.get("id"),
            "total_issues": obj.get("total_issues"),
            "cancelled_issues": obj.get("cancelled_issues"),
            "completed_issues": obj.get("completed_issues"),
            "started_issues": obj.get("started_issues"),
            "unstarted_issues": obj.get("unstarted_issues"),
            "backlog_issues": obj.get("backlog_issues"),
            "total_estimates": obj.get("total_estimates"),
            "completed_estimates": obj.get("completed_estimates"),
            "started_estimates": obj.get("started_estimates"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "start_date": obj.get("start_date"),
            "end_date": obj.get("end_date"),
            "view_props": obj.get("view_props"),
            "sort_order": obj.get("sort_order"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "progress_snapshot": obj.get("progress_snapshot"),
            "archived_at": obj.get("archived_at"),
            "logo_props": obj.get("logo_props"),
            "timezone": obj.get("timezone"),
            "version": obj.get("version"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "owned_by": obj.get("owned_by")
        })
        return _obj


