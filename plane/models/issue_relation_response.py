# coding: utf-8

"""
    The Plane REST API

    The Plane REST API  Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

    The version of the API Spec: 0.0.2
    Contact: support@plane.so
    This class is auto generated.

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set
from typing_extensions import Self

class IssueRelationResponse(BaseModel):
    """
    Serializer for issue relations response showing grouped relation types.  Returns issue IDs organized by relation type for efficient client-side processing.
    """ # noqa: E501
    blocking: List[StrictStr] = Field(description="List of issue IDs that are blocking this issue")
    blocked_by: List[StrictStr] = Field(description="List of issue IDs that this issue is blocked by")
    duplicate: List[StrictStr] = Field(description="List of issue IDs that are duplicates of this issue")
    relates_to: List[StrictStr] = Field(description="List of issue IDs that relate to this issue")
    start_after: List[StrictStr] = Field(description="List of issue IDs that start after this issue")
    start_before: List[StrictStr] = Field(description="List of issue IDs that start before this issue")
    finish_after: List[StrictStr] = Field(description="List of issue IDs that finish after this issue")
    finish_before: List[StrictStr] = Field(description="List of issue IDs that finish before this issue")
    __properties: ClassVar[List[str]] = ["blocking", "blocked_by", "duplicate", "relates_to", "start_after", "start_before", "finish_after", "finish_before"]

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
        """Create an instance of IssueRelationResponse from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IssueRelationResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "blocking": obj.get("blocking"),
            "blocked_by": obj.get("blocked_by"),
            "duplicate": obj.get("duplicate"),
            "relates_to": obj.get("relates_to"),
            "start_after": obj.get("start_after"),
            "start_before": obj.get("start_before"),
            "finish_after": obj.get("finish_after"),
            "finish_before": obj.get("finish_before")
        })
        return _obj


