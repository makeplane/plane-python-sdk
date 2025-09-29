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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Set
from typing_extensions import Self

class IssueRelation(BaseModel):
    """
    Serializer for issue relationships showing related issue details.  Provides comprehensive information about related issues including project context, sequence ID, and relationship type.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    project_id: Optional[StrictStr] = None
    sequence_id: Optional[StrictInt] = None
    relation_type: Optional[StrictStr] = None
    name: Optional[StrictStr] = None
    type_id: Optional[StrictStr] = None
    is_epic: Optional[StrictBool] = None
    state_id: Optional[StrictStr] = None
    priority: Optional[StrictStr] = None
    created_by: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["id", "project_id", "sequence_id", "relation_type", "name", "type_id", "is_epic", "state_id", "priority", "created_by", "created_at", "updated_at", "updated_by"]

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
        """Create an instance of IssueRelation from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "project_id",
            "sequence_id",
            "relation_type",
            "name",
            "type_id",
            "is_epic",
            "state_id",
            "priority",
            "created_by",
            "created_at",
            "updated_at",
            "updated_by",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
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
        """Create an instance of IssueRelation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "project_id": obj.get("project_id"),
            "sequence_id": obj.get("sequence_id"),
            "relation_type": obj.get("relation_type"),
            "name": obj.get("name"),
            "type_id": obj.get("type_id"),
            "is_epic": obj.get("is_epic"),
            "state_id": obj.get("state_id"),
            "priority": obj.get("priority"),
            "created_by": obj.get("created_by"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "updated_by": obj.get("updated_by")
        })
        return _obj


