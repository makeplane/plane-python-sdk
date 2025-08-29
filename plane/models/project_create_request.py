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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from plane.models.timezone_enum import TimezoneEnum
from typing import Set
from typing_extensions import Self

class ProjectCreateRequest(BaseModel):
    """
    Serializer for creating projects with workspace validation.  Handles project creation including identifier validation, member verification, and workspace association for new project initialization.
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True, max_length=255)]
    description: Optional[StrictStr] = None
    project_lead: Optional[StrictStr] = None
    default_assignee: Optional[StrictStr] = None
    identifier: Annotated[str, Field(min_length=1, strict=True, max_length=12)]
    icon_prop: Optional[Any] = None
    emoji: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    cover_image: Optional[StrictStr] = None
    module_view: Optional[StrictBool] = None
    cycle_view: Optional[StrictBool] = None
    issue_views_view: Optional[StrictBool] = None
    page_view: Optional[StrictBool] = None
    intake_view: Optional[StrictBool] = None
    guest_view_all_features: Optional[StrictBool] = None
    archive_in: Optional[Annotated[int, Field(le=12, strict=True, ge=0)]] = None
    close_in: Optional[Annotated[int, Field(le=12, strict=True, ge=0)]] = None
    timezone: Optional[TimezoneEnum] = None
    __properties: ClassVar[List[str]] = ["name", "description", "project_lead", "default_assignee", "identifier", "icon_prop", "emoji", "cover_image", "module_view", "cycle_view", "issue_views_view", "page_view", "intake_view", "guest_view_all_features", "archive_in", "close_in", "timezone"]

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
        """Create an instance of ProjectCreateRequest from a JSON string"""
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
        # set to None if project_lead (nullable) is None
        # and model_fields_set contains the field
        if self.project_lead is None and "project_lead" in self.model_fields_set:
            _dict['project_lead'] = None

        # set to None if default_assignee (nullable) is None
        # and model_fields_set contains the field
        if self.default_assignee is None and "default_assignee" in self.model_fields_set:
            _dict['default_assignee'] = None

        # set to None if icon_prop (nullable) is None
        # and model_fields_set contains the field
        if self.icon_prop is None and "icon_prop" in self.model_fields_set:
            _dict['icon_prop'] = None

        # set to None if emoji (nullable) is None
        # and model_fields_set contains the field
        if self.emoji is None and "emoji" in self.model_fields_set:
            _dict['emoji'] = None

        # set to None if cover_image (nullable) is None
        # and model_fields_set contains the field
        if self.cover_image is None and "cover_image" in self.model_fields_set:
            _dict['cover_image'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectCreateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "project_lead": obj.get("project_lead"),
            "default_assignee": obj.get("default_assignee"),
            "identifier": obj.get("identifier"),
            "icon_prop": obj.get("icon_prop"),
            "emoji": obj.get("emoji"),
            "cover_image": obj.get("cover_image"),
            "module_view": obj.get("module_view"),
            "cycle_view": obj.get("cycle_view"),
            "issue_views_view": obj.get("issue_views_view"),
            "page_view": obj.get("page_view"),
            "intake_view": obj.get("intake_view"),
            "guest_view_all_features": obj.get("guest_view_all_features"),
            "archive_in": obj.get("archive_in"),
            "close_in": obj.get("close_in"),
            "timezone": obj.get("timezone")
        })
        return _obj


