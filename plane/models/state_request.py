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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, constr
from plane.models.group_enum import GroupEnum

class StateRequest(BaseModel):
    """
    Serializer for work item states with default state management.  Handles state creation and updates including default state validation and automatic default state switching for workflow management.  # noqa: E501
    """
    name: constr(strict=True, max_length=255, min_length=1) = Field(...)
    description: Optional[StrictStr] = None
    color: constr(strict=True, max_length=255, min_length=1) = Field(...)
    sequence: Optional[Union[StrictFloat, StrictInt]] = None
    group: Optional[GroupEnum] = None
    is_triage: Optional[StrictBool] = None
    default: Optional[StrictBool] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    __properties = ["name", "description", "color", "sequence", "group", "is_triage", "default", "external_source", "external_id"]

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
    def from_json(cls, json_str: str) -> StateRequest:
        """Create an instance of StateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if external_source (nullable) is None
        # and __fields_set__ contains the field
        if self.external_source is None and "external_source" in self.__fields_set__:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and __fields_set__ contains the field
        if self.external_id is None and "external_id" in self.__fields_set__:
            _dict['external_id'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StateRequest:
        """Create an instance of StateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StateRequest.parse_obj(obj)

        _obj = StateRequest.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "color": obj.get("color"),
            "sequence": obj.get("sequence"),
            "group": obj.get("group"),
            "is_triage": obj.get("is_triage"),
            "default": obj.get("default"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id")
        })
        return _obj


