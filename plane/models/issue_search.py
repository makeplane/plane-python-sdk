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


from pydantic import BaseModel, Field, conlist
from plane.models.issue_search_item import IssueSearchItem

class IssueSearch(BaseModel):
    """
    Search results for work items.  Provides list of issues with their identifiers, names, and project context.  # noqa: E501
    """
    issues: conlist(IssueSearchItem) = Field(...)
    __properties = ["issues"]

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
    def from_json(cls, json_str: str) -> IssueSearch:
        """Create an instance of IssueSearch from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in issues (list)
        _items = []
        if self.issues:
            for _item in self.issues:
                if _item:
                    _items.append(_item.to_dict())
            _dict['issues'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueSearch:
        """Create an instance of IssueSearch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueSearch.parse_obj(obj)

        _obj = IssueSearch.parse_obj({
            "issues": [IssueSearchItem.from_dict(_item) for _item in obj.get("issues")] if obj.get("issues") is not None else None
        })
        return _obj


