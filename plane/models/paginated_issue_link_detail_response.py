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

from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from plane.models.issue_link import IssueLink
from typing import Set
from typing_extensions import Self

class PaginatedIssueLinkDetailResponse(BaseModel):
    """
    PaginatedIssueLinkDetailResponse
    """ # noqa: E501
    grouped_by: Optional[StrictStr]
    sub_grouped_by: Optional[StrictStr]
    total_count: StrictInt
    next_cursor: StrictStr
    prev_cursor: StrictStr
    next_page_results: StrictBool
    prev_page_results: StrictBool
    count: StrictInt
    total_pages: StrictInt
    total_results: StrictInt
    extra_stats: Optional[StrictStr]
    results: List[IssueLink]
    __properties: ClassVar[List[str]] = ["grouped_by", "sub_grouped_by", "total_count", "next_cursor", "prev_cursor", "next_page_results", "prev_page_results", "count", "total_pages", "total_results", "extra_stats", "results"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of PaginatedIssueLinkDetailResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in results (list)
        _items = []
        if self.results:
            for _item_results in self.results:
                if _item_results:
                    _items.append(_item_results.to_dict())
            _dict['results'] = _items
        # set to None if grouped_by (nullable) is None
        # and model_fields_set contains the field
        if self.grouped_by is None and "grouped_by" in self.model_fields_set:
            _dict['grouped_by'] = None

        # set to None if sub_grouped_by (nullable) is None
        # and model_fields_set contains the field
        if self.sub_grouped_by is None and "sub_grouped_by" in self.model_fields_set:
            _dict['sub_grouped_by'] = None

        # set to None if extra_stats (nullable) is None
        # and model_fields_set contains the field
        if self.extra_stats is None and "extra_stats" in self.model_fields_set:
            _dict['extra_stats'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PaginatedIssueLinkDetailResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
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
            "results": [IssueLink.from_dict(_item) for _item in obj["results"]] if obj.get("results") is not None else None
        })
        return _obj


