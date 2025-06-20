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
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist, constr

class IssueTypeAPI(BaseModel):
    """
    IssueTypeAPI
    """
    id: Optional[StrictStr] = None
    deleted_at: Optional[datetime] = None
    project_ids: Optional[conlist(StrictStr)] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    name: constr(strict=True, max_length=255) = Field(...)
    description: Optional[StrictStr] = None
    logo_props: Optional[Any] = None
    is_epic: Optional[StrictBool] = None
    is_default: Optional[StrictBool] = None
    is_active: Optional[StrictBool] = None
    level: Optional[Union[StrictFloat, StrictInt]] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    __properties = ["id", "deleted_at", "project_ids", "created_at", "updated_at", "name", "description", "logo_props", "is_epic", "is_default", "is_active", "level", "external_source", "external_id", "created_by", "updated_by", "workspace"]

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
    def from_json(cls, json_str: str) -> IssueTypeAPI:
        """Create an instance of IssueTypeAPI from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "deleted_at",
                            "created_at",
                            "updated_at",
                            "logo_props",
                            "is_default",
                            "level",
                            "created_by",
                            "updated_by",
                            "workspace",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if logo_props (nullable) is None
        # and __fields_set__ contains the field
        if self.logo_props is None and "logo_props" in self.__fields_set__:
            _dict['logo_props'] = None

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

        # set to None if updated_by (nullable) is None
        # and __fields_set__ contains the field
        if self.updated_by is None and "updated_by" in self.__fields_set__:
            _dict['updated_by'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueTypeAPI:
        """Create an instance of IssueTypeAPI from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueTypeAPI.parse_obj(obj)

        _obj = IssueTypeAPI.parse_obj({
            "id": obj.get("id"),
            "deleted_at": obj.get("deleted_at"),
            "project_ids": obj.get("project_ids"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "logo_props": obj.get("logo_props"),
            "is_epic": obj.get("is_epic"),
            "is_default": obj.get("is_default"),
            "is_active": obj.get("is_active"),
            "level": obj.get("level"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "workspace": obj.get("workspace")
        })
        return _obj


