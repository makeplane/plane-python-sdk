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

from datetime import date
from typing import Optional
from pydantic import BaseModel, StrictStr, conlist, constr
from plane.models.module_status_enum import ModuleStatusEnum

class PatchedModuleUpdateRequest(BaseModel):
    """
    Serializer for updating modules with enhanced validation and member management.  Extends module creation with update-specific validations including member reassignment, name conflict checking, and relationship management for module modifications.  # noqa: E501
    """
    name: Optional[constr(strict=True, max_length=255, min_length=1)] = None
    description: Optional[StrictStr] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    status: Optional[ModuleStatusEnum] = None
    lead: Optional[StrictStr] = None
    members: Optional[conlist(StrictStr)] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    __properties = ["name", "description", "start_date", "target_date", "status", "lead", "members", "external_source", "external_id"]

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
    def from_json(cls, json_str: str) -> PatchedModuleUpdateRequest:
        """Create an instance of PatchedModuleUpdateRequest from a JSON string"""
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

        # set to None if target_date (nullable) is None
        # and __fields_set__ contains the field
        if self.target_date is None and "target_date" in self.__fields_set__:
            _dict['target_date'] = None

        # set to None if lead (nullable) is None
        # and __fields_set__ contains the field
        if self.lead is None and "lead" in self.__fields_set__:
            _dict['lead'] = None

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
    def from_dict(cls, obj: dict) -> PatchedModuleUpdateRequest:
        """Create an instance of PatchedModuleUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedModuleUpdateRequest.parse_obj(obj)

        _obj = PatchedModuleUpdateRequest.parse_obj({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "start_date": obj.get("start_date"),
            "target_date": obj.get("target_date"),
            "status": obj.get("status"),
            "lead": obj.get("lead"),
            "members": obj.get("members"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id")
        })
        return _obj


