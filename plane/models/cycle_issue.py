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
from pydantic import BaseModel, ConfigDict, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Set
from typing_extensions import Self

class CycleIssue(BaseModel):
    """
    Serializer for cycle-issue relationships with sub-issue counting.  Manages the association between cycles and work items, including hierarchical issue tracking for nested work item structures.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    sub_issues_count: Optional[StrictInt] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime]
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    issue: StrictStr
    cycle: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["id", "sub_issues_count", "created_at", "updated_at", "deleted_at", "created_by", "updated_by", "project", "workspace", "issue", "cycle"]

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
        """Create an instance of CycleIssue from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "sub_issues_count",
            "created_at",
            "updated_at",
            "project",
            "workspace",
            "cycle",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if deleted_at (nullable) is None
        # and model_fields_set contains the field
        if self.deleted_at is None and "deleted_at" in self.model_fields_set:
            _dict['deleted_at'] = None

        # set to None if created_by (nullable) is None
        # and model_fields_set contains the field
        if self.created_by is None and "created_by" in self.model_fields_set:
            _dict['created_by'] = None

        # set to None if updated_by (nullable) is None
        # and model_fields_set contains the field
        if self.updated_by is None and "updated_by" in self.model_fields_set:
            _dict['updated_by'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CycleIssue from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "sub_issues_count": obj.get("sub_issues_count"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "issue": obj.get("issue"),
            "cycle": obj.get("cycle")
        })
        return _obj


