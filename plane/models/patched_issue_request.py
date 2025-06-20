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
from typing import Optional, Union
from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr, conint, conlist, constr
from plane.models.priority_enum import PriorityEnum

class PatchedIssueRequest(BaseModel):
    """
    Comprehensive work item serializer with full relationship management.  Handles complete work item lifecycle including assignees, labels, validation, and related model updates. Supports dynamic field expansion and HTML content processing.  # noqa: E501
    """
    assignees: Optional[conlist(StrictStr)] = None
    labels: Optional[conlist(StrictStr)] = None
    type_id: Optional[StrictStr] = None
    deleted_at: Optional[datetime] = None
    point: Optional[conint(strict=True, le=12, ge=0)] = None
    name: Optional[constr(strict=True, max_length=255, min_length=1)] = None
    description_html: Optional[StrictStr] = None
    description_stripped: Optional[StrictStr] = None
    priority: Optional[PriorityEnum] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    sequence_id: Optional[conint(strict=True, le=2147483647, ge=-2147483648)] = None
    sort_order: Optional[Union[StrictFloat, StrictInt]] = None
    completed_at: Optional[datetime] = None
    archived_at: Optional[date] = None
    is_draft: Optional[StrictBool] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    created_by: Optional[StrictStr] = None
    parent: Optional[StrictStr] = None
    state: Optional[StrictStr] = None
    estimate_point: Optional[StrictStr] = None
    type: Optional[StrictStr] = None
    __properties = ["assignees", "labels", "type_id", "deleted_at", "point", "name", "description_html", "description_stripped", "priority", "start_date", "target_date", "sequence_id", "sort_order", "completed_at", "archived_at", "is_draft", "external_source", "external_id", "created_by", "parent", "state", "estimate_point", "type"]

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
    def from_json(cls, json_str: str) -> PatchedIssueRequest:
        """Create an instance of PatchedIssueRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if type_id (nullable) is None
        # and __fields_set__ contains the field
        if self.type_id is None and "type_id" in self.__fields_set__:
            _dict['type_id'] = None

        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if point (nullable) is None
        # and __fields_set__ contains the field
        if self.point is None and "point" in self.__fields_set__:
            _dict['point'] = None

        # set to None if description_stripped (nullable) is None
        # and __fields_set__ contains the field
        if self.description_stripped is None and "description_stripped" in self.__fields_set__:
            _dict['description_stripped'] = None

        # set to None if start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.start_date is None and "start_date" in self.__fields_set__:
            _dict['start_date'] = None

        # set to None if target_date (nullable) is None
        # and __fields_set__ contains the field
        if self.target_date is None and "target_date" in self.__fields_set__:
            _dict['target_date'] = None

        # set to None if completed_at (nullable) is None
        # and __fields_set__ contains the field
        if self.completed_at is None and "completed_at" in self.__fields_set__:
            _dict['completed_at'] = None

        # set to None if archived_at (nullable) is None
        # and __fields_set__ contains the field
        if self.archived_at is None and "archived_at" in self.__fields_set__:
            _dict['archived_at'] = None

        # set to None if external_source (nullable) is None
        # and __fields_set__ contains the field
        if self.external_source is None and "external_source" in self.__fields_set__:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and __fields_set__ contains the field
        if self.external_id is None and "external_id" in self.__fields_set__:
            _dict['external_id'] = None

        # set to None if created_by (nullable) is None
        # and __fields_set__ contains the field
        if self.created_by is None and "created_by" in self.__fields_set__:
            _dict['created_by'] = None

        # set to None if parent (nullable) is None
        # and __fields_set__ contains the field
        if self.parent is None and "parent" in self.__fields_set__:
            _dict['parent'] = None

        # set to None if state (nullable) is None
        # and __fields_set__ contains the field
        if self.state is None and "state" in self.__fields_set__:
            _dict['state'] = None

        # set to None if estimate_point (nullable) is None
        # and __fields_set__ contains the field
        if self.estimate_point is None and "estimate_point" in self.__fields_set__:
            _dict['estimate_point'] = None

        # set to None if type (nullable) is None
        # and __fields_set__ contains the field
        if self.type is None and "type" in self.__fields_set__:
            _dict['type'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PatchedIssueRequest:
        """Create an instance of PatchedIssueRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedIssueRequest.parse_obj(obj)

        _obj = PatchedIssueRequest.parse_obj({
            "assignees": obj.get("assignees"),
            "labels": obj.get("labels"),
            "type_id": obj.get("type_id"),
            "deleted_at": obj.get("deleted_at"),
            "point": obj.get("point"),
            "name": obj.get("name"),
            "description_html": obj.get("description_html"),
            "description_stripped": obj.get("description_stripped"),
            "priority": obj.get("priority"),
            "start_date": obj.get("start_date"),
            "target_date": obj.get("target_date"),
            "sequence_id": obj.get("sequence_id"),
            "sort_order": obj.get("sort_order"),
            "completed_at": obj.get("completed_at"),
            "archived_at": obj.get("archived_at"),
            "is_draft": obj.get("is_draft"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "created_by": obj.get("created_by"),
            "parent": obj.get("parent"),
            "state": obj.get("state"),
            "estimate_point": obj.get("estimate_point"),
            "type": obj.get("type")
        })
        return _obj


