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
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from typing import Set
from typing_extensions import Self

class IssueActivity(BaseModel):
    """
    Serializer for work item activity and change history.  Tracks and represents work item modifications, state changes, and user interactions for audit trails and activity feeds.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    verb: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    var_field: Optional[Annotated[str, Field(strict=True, max_length=255)]] = Field(default=None, alias="field")
    old_value: Optional[StrictStr] = None
    new_value: Optional[StrictStr] = None
    comment: Optional[StrictStr] = None
    attachments: Optional[Annotated[List[Annotated[str, Field(strict=True, max_length=200)]], Field(max_length=10)]] = None
    old_identifier: Optional[StrictStr] = None
    new_identifier: Optional[StrictStr] = None
    epoch: Optional[Union[StrictFloat, StrictInt]] = None
    project: StrictStr
    workspace: StrictStr
    issue: Optional[StrictStr] = None
    issue_comment: Optional[StrictStr] = None
    actor: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["id", "created_at", "updated_at", "deleted_at", "verb", "field", "old_value", "new_value", "comment", "attachments", "old_identifier", "new_identifier", "epoch", "project", "workspace", "issue", "issue_comment", "actor"]

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
        """Create an instance of IssueActivity from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "id",
            "created_at",
            "updated_at",
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

        # set to None if var_field (nullable) is None
        # and model_fields_set contains the field
        if self.var_field is None and "var_field" in self.model_fields_set:
            _dict['field'] = None

        # set to None if old_value (nullable) is None
        # and model_fields_set contains the field
        if self.old_value is None and "old_value" in self.model_fields_set:
            _dict['old_value'] = None

        # set to None if new_value (nullable) is None
        # and model_fields_set contains the field
        if self.new_value is None and "new_value" in self.model_fields_set:
            _dict['new_value'] = None

        # set to None if old_identifier (nullable) is None
        # and model_fields_set contains the field
        if self.old_identifier is None and "old_identifier" in self.model_fields_set:
            _dict['old_identifier'] = None

        # set to None if new_identifier (nullable) is None
        # and model_fields_set contains the field
        if self.new_identifier is None and "new_identifier" in self.model_fields_set:
            _dict['new_identifier'] = None

        # set to None if epoch (nullable) is None
        # and model_fields_set contains the field
        if self.epoch is None and "epoch" in self.model_fields_set:
            _dict['epoch'] = None

        # set to None if issue (nullable) is None
        # and model_fields_set contains the field
        if self.issue is None and "issue" in self.model_fields_set:
            _dict['issue'] = None

        # set to None if issue_comment (nullable) is None
        # and model_fields_set contains the field
        if self.issue_comment is None and "issue_comment" in self.model_fields_set:
            _dict['issue_comment'] = None

        # set to None if actor (nullable) is None
        # and model_fields_set contains the field
        if self.actor is None and "actor" in self.model_fields_set:
            _dict['actor'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IssueActivity from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "verb": obj.get("verb"),
            "field": obj.get("field"),
            "old_value": obj.get("old_value"),
            "new_value": obj.get("new_value"),
            "comment": obj.get("comment"),
            "attachments": obj.get("attachments"),
            "old_identifier": obj.get("old_identifier"),
            "new_identifier": obj.get("new_identifier"),
            "epoch": obj.get("epoch"),
            "project": obj.get("project"),
            "workspace": obj.get("workspace"),
            "issue": obj.get("issue"),
            "issue_comment": obj.get("issue_comment"),
            "actor": obj.get("actor")
        })
        return _obj


