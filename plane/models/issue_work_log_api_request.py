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


from typing import Optional
from pydantic import BaseModel, StrictStr, conint

class IssueWorkLogAPIRequest(BaseModel):
    """
    IssueWorkLogAPIRequest
    """
    description: Optional[StrictStr] = None
    duration: Optional[conint(strict=True, le=2147483647, ge=-2147483648)] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    __properties = ["description", "duration", "created_by", "updated_by"]

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
    def from_json(cls, json_str: str) -> IssueWorkLogAPIRequest:
        """Create an instance of IssueWorkLogAPIRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
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
    def from_dict(cls, obj: dict) -> IssueWorkLogAPIRequest:
        """Create an instance of IssueWorkLogAPIRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueWorkLogAPIRequest.parse_obj(obj)

        _obj = IssueWorkLogAPIRequest.parse_obj({
            "description": obj.get("description"),
            "duration": obj.get("duration"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by")
        })
        return _obj


