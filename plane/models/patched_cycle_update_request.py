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
from pydantic import BaseModel, StrictStr, constr
from plane.models.timezone_enum import TimezoneEnum

class PatchedCycleUpdateRequest(BaseModel):
    """
    Serializer for updating cycles with enhanced ownership management.  Extends cycle creation with update-specific features including ownership assignment and modification tracking for cycle lifecycle management.  # noqa: E501
    """
    name: Optional[constr(strict=True, max_length=255, min_length=1)] = None
    description: Optional[StrictStr] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    owned_by: Optional[StrictStr] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    timezone: Optional[TimezoneEnum] = None
    __properties = ["name", "description", "start_date", "end_date", "owned_by", "external_source", "external_id", "timezone"]

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
    def from_json(cls, json_str: str) -> PatchedCycleUpdateRequest:
        """Create an instance of PatchedCycleUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if start_date (nullable) is None
        # and __fields_set__ contains the field
        if self.start_date is None and "start_date" in self.__fields_set__:
            _dict['start_date'] = None

        # set to None if end_date (nullable) is None
        # and __fields_set__ contains the field
        if self.end_date is None and "end_date" in self.__fields_set__:
            _dict['end_date'] = None

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
    def from_dict(cls, obj: dict) -> PatchedCycleUpdateRequest:
        """Create an instance of PatchedCycleUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedCycleUpdateRequest.parse_obj(obj)

        _obj = PatchedCycleUpdateRequest.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "start_date": obj.get("start_date"),
            "end_date": obj.get("end_date"),
            "owned_by": obj.get("owned_by"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "timezone": obj.get("timezone")
        })
        return _obj


