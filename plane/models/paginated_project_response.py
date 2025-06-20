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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, conlist
from plane.models.project import Project

class PaginatedProjectResponse(BaseModel):
    """
    PaginatedProjectResponse
    """
    grouped_by: Optional[StrictStr] = Field(...)
    sub_grouped_by: Optional[StrictStr] = Field(...)
    total_count: StrictInt = Field(...)
    next_cursor: StrictStr = Field(...)
    prev_cursor: StrictStr = Field(...)
    next_page_results: StrictBool = Field(...)
    prev_page_results: StrictBool = Field(...)
    count: StrictInt = Field(...)
    total_pages: StrictInt = Field(...)
    total_results: StrictInt = Field(...)
    extra_stats: Optional[StrictStr] = Field(...)
    results: conlist(Project) = Field(...)
    __properties = ["grouped_by", "sub_grouped_by", "total_count", "next_cursor", "prev_cursor", "next_page_results", "prev_page_results", "count", "total_pages", "total_results", "extra_stats", "results"]

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
    def from_json(cls, json_str: str) -> PaginatedProjectResponse:
        """Create an instance of PaginatedProjectResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in results (list)
        _items = []
        if self.results:
            for _item in self.results:
                if _item:
                    _items.append(_item.to_dict())
            _dict['results'] = _items
        # set to None if grouped_by (nullable) is None
        # and __fields_set__ contains the field
        if self.grouped_by is None and "grouped_by" in self.__fields_set__:
            _dict['grouped_by'] = None

        # set to None if sub_grouped_by (nullable) is None
        # and __fields_set__ contains the field
        if self.sub_grouped_by is None and "sub_grouped_by" in self.__fields_set__:
            _dict['sub_grouped_by'] = None

        # set to None if extra_stats (nullable) is None
        # and __fields_set__ contains the field
        if self.extra_stats is None and "extra_stats" in self.__fields_set__:
            _dict['extra_stats'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PaginatedProjectResponse:
        """Create an instance of PaginatedProjectResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PaginatedProjectResponse.parse_obj(obj)

        _obj = PaginatedProjectResponse.parse_obj({
            "grouped_by": obj.get("grouped_by"),
            "sub_grouped_by": obj.get("sub_grouped_by"),
            "total_count": obj.get("total_count"),
            "next_cursor": obj.get("next_cursor"),
            "prev_cursor": obj.get("prev_cursor"),
            "next_page_results": obj.get("next_page_results"),
            "prev_page_results": obj.get("prev_page_results"),
            "count": obj.get("count"),
            "total_pages": obj.get("total_pages"),
            "total_results": obj.get("total_results"),
            "extra_stats": obj.get("extra_stats"),
            "results": [Project.from_dict(_item) for _item in obj.get("results")] if obj.get("results") is not None else None
        })
        return _obj


