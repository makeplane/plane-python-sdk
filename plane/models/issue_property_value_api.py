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
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, constr

class IssuePropertyValueAPI(BaseModel):
    """
    IssuePropertyValueAPI
    """
    id: Optional[StrictStr] = None
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    value_text: Optional[StrictStr] = None
    value_boolean: Optional[StrictBool] = None
    value_decimal: Optional[Union[StrictFloat, StrictInt]] = None
    value_datetime: Optional[datetime] = None
    value_uuid: Optional[StrictStr] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    issue: StrictStr = Field(...)
    var_property: StrictStr = Field(default=..., alias="property")
    value_option: Optional[StrictStr] = None
    __properties = ["id", "deleted_at", "created_at", "updated_at", "value_text", "value_boolean", "value_decimal", "value_datetime", "value_uuid", "external_source", "external_id", "created_by", "updated_by", "workspace", "project", "issue", "property", "value_option"]

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
    def from_json(cls, json_str: str) -> IssuePropertyValueAPI:
        """Create an instance of IssuePropertyValueAPI from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "deleted_at",
                            "created_at",
                            "updated_at",
                            "created_by",
                            "updated_by",
                            "workspace",
                            "project",
                          },
                          exclude_none=True)
        # set to None if deleted_at (nullable) is None
        # and __fields_set__ contains the field
        if self.deleted_at is None and "deleted_at" in self.__fields_set__:
            _dict['deleted_at'] = None

        # set to None if value_datetime (nullable) is None
        # and __fields_set__ contains the field
        if self.value_datetime is None and "value_datetime" in self.__fields_set__:
            _dict['value_datetime'] = None

        # set to None if value_uuid (nullable) is None
        # and __fields_set__ contains the field
        if self.value_uuid is None and "value_uuid" in self.__fields_set__:
            _dict['value_uuid'] = None

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

        # set to None if project (nullable) is None
        # and __fields_set__ contains the field
        if self.project is None and "project" in self.__fields_set__:
            _dict['project'] = None

        # set to None if value_option (nullable) is None
        # and __fields_set__ contains the field
        if self.value_option is None and "value_option" in self.__fields_set__:
            _dict['value_option'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssuePropertyValueAPI:
        """Create an instance of IssuePropertyValueAPI from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssuePropertyValueAPI.parse_obj(obj)

        _obj = IssuePropertyValueAPI.parse_obj({
            "id": obj.get("id"),
            "deleted_at": obj.get("deleted_at"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "value_text": obj.get("value_text"),
            "value_boolean": obj.get("value_boolean"),
            "value_decimal": obj.get("value_decimal"),
            "value_datetime": obj.get("value_datetime"),
            "value_uuid": obj.get("value_uuid"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "workspace": obj.get("workspace"),
            "project": obj.get("project"),
            "issue": obj.get("issue"),
            "var_property": obj.get("property"),
            "value_option": obj.get("value_option")
        })
        return _obj


