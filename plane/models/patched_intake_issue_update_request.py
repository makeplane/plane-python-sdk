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
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from plane.models.intake_work_item_status_enum import IntakeWorkItemStatusEnum
from plane.models.issue_for_intake_request import IssueForIntakeRequest
from typing import Set
from typing_extensions import Self

class PatchedIntakeIssueUpdateRequest(BaseModel):
    """
    Serializer for updating intake work items and their associated issues.  Handles intake work item modifications including status changes, triage decisions, and embedded issue updates for issue queue processing workflows.
    """ # noqa: E501
    status: Optional[IntakeWorkItemStatusEnum] = None
    snoozed_till: Optional[datetime] = None
    duplicate_to: Optional[StrictStr] = None
    source: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    source_email: Optional[StrictStr] = None
    issue: Optional[IssueForIntakeRequest] = Field(default=None, description="Issue data to update in the intake issue")
    __properties: ClassVar[List[str]] = ["status", "snoozed_till", "duplicate_to", "source", "source_email", "issue"]

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
        """Create an instance of PatchedIntakeIssueUpdateRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of issue
        if self.issue:
            _dict['issue'] = self.issue.to_dict()
        # set to None if snoozed_till (nullable) is None
        # and model_fields_set contains the field
        if self.snoozed_till is None and "snoozed_till" in self.model_fields_set:
            _dict['snoozed_till'] = None

        # set to None if duplicate_to (nullable) is None
        # and model_fields_set contains the field
        if self.duplicate_to is None and "duplicate_to" in self.model_fields_set:
            _dict['duplicate_to'] = None

        # set to None if source (nullable) is None
        # and model_fields_set contains the field
        if self.source is None and "source" in self.model_fields_set:
            _dict['source'] = None

        # set to None if source_email (nullable) is None
        # and model_fields_set contains the field
        if self.source_email is None and "source_email" in self.model_fields_set:
            _dict['source_email'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchedIntakeIssueUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "status": obj.get("status"),
            "snoozed_till": obj.get("snoozed_till"),
            "duplicate_to": obj.get("duplicate_to"),
            "source": obj.get("source"),
            "source_email": obj.get("source_email"),
            "issue": IssueForIntakeRequest.from_dict(obj["issue"]) if obj.get("issue") is not None else None
        })
        return _obj


