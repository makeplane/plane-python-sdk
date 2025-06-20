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
from pydantic import BaseModel, StrictBool, StrictStr, conlist, constr
from plane.models.property_type_enum import PropertyTypeEnum
from plane.models.relation_type_enum import RelationTypeEnum

class PatchedIssuePropertyAPIRequest(BaseModel):
    """
    PatchedIssuePropertyAPIRequest
    """
    relation_type: Optional[RelationTypeEnum] = None
    display_name: Optional[constr(strict=True, max_length=255, min_length=1)] = None
    description: Optional[StrictStr] = None
    property_type: Optional[PropertyTypeEnum] = None
    is_required: Optional[StrictBool] = None
    default_value: Optional[conlist(constr(strict=True, min_length=1))] = None
    settings: Optional[Any] = None
    is_active: Optional[StrictBool] = None
    is_multi: Optional[StrictBool] = None
    validation_rules: Optional[Any] = None
    external_source: Optional[constr(strict=True, max_length=255)] = None
    external_id: Optional[constr(strict=True, max_length=255)] = None
    __properties = ["relation_type", "display_name", "description", "property_type", "is_required", "default_value", "settings", "is_active", "is_multi", "validation_rules", "external_source", "external_id"]

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
    def from_json(cls, json_str: str) -> PatchedIssuePropertyAPIRequest:
        """Create an instance of PatchedIssuePropertyAPIRequest from a JSON string"""
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

        # set to None if settings (nullable) is None
        # and __fields_set__ contains the field
        if self.settings is None and "settings" in self.__fields_set__:
            _dict['settings'] = None

        # set to None if validation_rules (nullable) is None
        # and __fields_set__ contains the field
        if self.validation_rules is None and "validation_rules" in self.__fields_set__:
            _dict['validation_rules'] = None

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
    def from_dict(cls, obj: dict) -> PatchedIssuePropertyAPIRequest:
        """Create an instance of PatchedIssuePropertyAPIRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PatchedIssuePropertyAPIRequest.parse_obj(obj)

        _obj = PatchedIssuePropertyAPIRequest.parse_obj({
            "relation_type": obj.get("relation_type"),
            "display_name": obj.get("display_name"),
            "description": obj.get("description"),
            "property_type": obj.get("property_type"),
            "is_required": obj.get("is_required"),
            "default_value": obj.get("default_value"),
            "settings": obj.get("settings"),
            "is_active": obj.get("is_active"),
            "is_multi": obj.get("is_multi"),
            "validation_rules": obj.get("validation_rules"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id")
        })
        return _obj


