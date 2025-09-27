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
from typing_extensions import Annotated
from plane.models.issue_relation_create_relation_type_enum import IssueRelationCreateRelationTypeEnum
from typing import Optional, Set
from typing_extensions import Self

class IssueRelationCreateRequest(BaseModel):
    """
    Serializer for creating issue relations.  Creates issue relations with the specified relation type and issues. Validates relation types and ensures proper issue ID format.
    """ # noqa: E501
    relation_type: IssueRelationCreateRelationTypeEnum = Field(description="Type of relationship between work items  * `blocking` - Blocking * `blocked_by` - Blocked By * `duplicate` - Duplicate * `relates_to` - Relates To * `start_before` - Start Before * `start_after` - Start After * `finish_before` - Finish Before * `finish_after` - Finish After")
    issues: Annotated[List[StrictStr], Field(min_length=1)] = Field(description="Array of work item IDs to create relations with")
    __properties: ClassVar[List[str]] = ["relation_type", "issues"]

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
        """Create an instance of IssueRelationCreateRequest from a JSON string"""
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
        """Create an instance of IssueRelationCreateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "relation_type": obj.get("relation_type"),
            "issues": obj.get("issues")
        })
        return _obj


