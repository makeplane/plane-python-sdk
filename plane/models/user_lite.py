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
from pydantic import BaseModel, Field, StrictStr

class UserLite(BaseModel):
    """
    Lightweight user serializer for minimal data transfer.  Provides essential user information including names, avatar, and contact details optimized for member lists, assignee displays, and user references.  # noqa: E501
    """
    id: Optional[StrictStr] = None
    first_name: Optional[StrictStr] = None
    last_name: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
    avatar: Optional[StrictStr] = None
    avatar_url: Optional[StrictStr] = Field(default=None, description="Avatar URL")
    display_name: Optional[StrictStr] = None
    __properties = ["id", "first_name", "last_name", "email", "avatar", "avatar_url", "display_name"]

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
    def from_json(cls, json_str: str) -> UserLite:
        """Create an instance of UserLite from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "id",
                            "first_name",
                            "last_name",
                            "email",
                            "avatar",
                            "avatar_url",
                            "display_name",
                          },
                          exclude_none=True)
        # set to None if email (nullable) is None
        # and __fields_set__ contains the field
        if self.email is None and "email" in self.__fields_set__:
            _dict['email'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UserLite:
        """Create an instance of UserLite from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UserLite.parse_obj(obj)

        _obj = UserLite.parse_obj({
            "id": obj.get("id"),
            "first_name": obj.get("first_name"),
            "last_name": obj.get("last_name"),
            "email": obj.get("email"),
            "avatar": obj.get("avatar"),
            "avatar_url": obj.get("avatar_url"),
            "display_name": obj.get("display_name")
        })
        return _obj


