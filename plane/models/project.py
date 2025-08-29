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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from plane.models.network_enum import NetworkEnum
from plane.models.timezone_enum import TimezoneEnum
from typing import Set
from typing_extensions import Self

class Project(BaseModel):
    """
    Comprehensive project serializer with metrics and member context.  Provides complete project data including member counts, cycle/module totals, deployment status, and user-specific context for project management.
    """ # noqa: E501
    id: Optional[StrictStr] = None
    total_members: Optional[StrictInt] = None
    total_cycles: Optional[StrictInt] = None
    total_modules: Optional[StrictInt] = None
    is_member: Optional[StrictBool] = None
    sort_order: Optional[Union[StrictFloat, StrictInt]] = None
    member_role: Optional[StrictInt] = None
    is_deployed: Optional[StrictBool] = None
    cover_image_url: Optional[StrictStr] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    name: Annotated[str, Field(strict=True, max_length=255)]
    description: Optional[StrictStr] = None
    description_text: Optional[Any] = None
    description_html: Optional[Any] = None
    network: Optional[NetworkEnum] = None
    identifier: Annotated[str, Field(strict=True, max_length=12)]
    emoji: Optional[StrictStr] = None
    icon_prop: Optional[Any] = None
    module_view: Optional[StrictBool] = None
    cycle_view: Optional[StrictBool] = None
    issue_views_view: Optional[StrictBool] = None
    page_view: Optional[StrictBool] = None
    intake_view: Optional[StrictBool] = None
    is_time_tracking_enabled: Optional[StrictBool] = None
    is_issue_type_enabled: Optional[StrictBool] = None
    guest_view_all_features: Optional[StrictBool] = None
    cover_image: Optional[StrictStr] = None
    archive_in: Optional[Annotated[int, Field(le=12, strict=True, ge=0)]] = None
    close_in: Optional[Annotated[int, Field(le=12, strict=True, ge=0)]] = None
    logo_props: Optional[Any] = None
    archived_at: Optional[datetime] = None
    timezone: Optional[TimezoneEnum] = None
    external_source: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    external_id: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    default_assignee: Optional[StrictStr] = None
    project_lead: Optional[StrictStr] = None
    cover_image_asset: Optional[StrictStr] = None
    estimate: Optional[StrictStr] = None
    default_state: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["id", "total_members", "total_cycles", "total_modules", "is_member", "sort_order", "member_role", "is_deployed", "cover_image_url", "created_at", "updated_at", "deleted_at", "name", "description", "description_text", "description_html", "network", "identifier", "emoji", "icon_prop", "module_view", "cycle_view", "issue_views_view", "page_view", "intake_view", "is_time_tracking_enabled", "is_issue_type_enabled", "guest_view_all_features", "cover_image", "archive_in", "close_in", "logo_props", "archived_at", "timezone", "external_source", "external_id", "created_by", "updated_by", "workspace", "default_assignee", "project_lead", "cover_image_asset", "estimate", "default_state"]

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
        """Create an instance of Project from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "total_members",
            "total_cycles",
            "total_modules",
            "is_member",
            "sort_order",
            "member_role",
            "is_deployed",
            "cover_image_url",
            "created_at",
            "updated_at",
            "deleted_at",
            "emoji",
            "created_by",
            "updated_by",
            "workspace",
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

        # set to None if description_text (nullable) is None
        # and model_fields_set contains the field
        if self.description_text is None and "description_text" in self.model_fields_set:
            _dict['description_text'] = None

        # set to None if description_html (nullable) is None
        # and model_fields_set contains the field
        if self.description_html is None and "description_html" in self.model_fields_set:
            _dict['description_html'] = None

        # set to None if emoji (nullable) is None
        # and model_fields_set contains the field
        if self.emoji is None and "emoji" in self.model_fields_set:
            _dict['emoji'] = None

        # set to None if icon_prop (nullable) is None
        # and model_fields_set contains the field
        if self.icon_prop is None and "icon_prop" in self.model_fields_set:
            _dict['icon_prop'] = None

        # set to None if cover_image (nullable) is None
        # and model_fields_set contains the field
        if self.cover_image is None and "cover_image" in self.model_fields_set:
            _dict['cover_image'] = None

        # set to None if logo_props (nullable) is None
        # and model_fields_set contains the field
        if self.logo_props is None and "logo_props" in self.model_fields_set:
            _dict['logo_props'] = None

        # set to None if archived_at (nullable) is None
        # and model_fields_set contains the field
        if self.archived_at is None and "archived_at" in self.model_fields_set:
            _dict['archived_at'] = None

        # set to None if external_source (nullable) is None
        # and model_fields_set contains the field
        if self.external_source is None and "external_source" in self.model_fields_set:
            _dict['external_source'] = None

        # set to None if external_id (nullable) is None
        # and model_fields_set contains the field
        if self.external_id is None and "external_id" in self.model_fields_set:
            _dict['external_id'] = None

        # set to None if created_by (nullable) is None
        # and model_fields_set contains the field
        if self.created_by is None and "created_by" in self.model_fields_set:
            _dict['created_by'] = None

        # set to None if updated_by (nullable) is None
        # and model_fields_set contains the field
        if self.updated_by is None and "updated_by" in self.model_fields_set:
            _dict['updated_by'] = None

        # set to None if default_assignee (nullable) is None
        # and model_fields_set contains the field
        if self.default_assignee is None and "default_assignee" in self.model_fields_set:
            _dict['default_assignee'] = None

        # set to None if project_lead (nullable) is None
        # and model_fields_set contains the field
        if self.project_lead is None and "project_lead" in self.model_fields_set:
            _dict['project_lead'] = None

        # set to None if cover_image_asset (nullable) is None
        # and model_fields_set contains the field
        if self.cover_image_asset is None and "cover_image_asset" in self.model_fields_set:
            _dict['cover_image_asset'] = None

        # set to None if estimate (nullable) is None
        # and model_fields_set contains the field
        if self.estimate is None and "estimate" in self.model_fields_set:
            _dict['estimate'] = None

        # set to None if default_state (nullable) is None
        # and model_fields_set contains the field
        if self.default_state is None and "default_state" in self.model_fields_set:
            _dict['default_state'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Project from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "total_members": obj.get("total_members"),
            "total_cycles": obj.get("total_cycles"),
            "total_modules": obj.get("total_modules"),
            "is_member": obj.get("is_member"),
            "sort_order": obj.get("sort_order"),
            "member_role": obj.get("member_role"),
            "is_deployed": obj.get("is_deployed"),
            "cover_image_url": obj.get("cover_image_url"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "deleted_at": obj.get("deleted_at"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "description_text": obj.get("description_text"),
            "description_html": obj.get("description_html"),
            "network": obj.get("network"),
            "identifier": obj.get("identifier"),
            "emoji": obj.get("emoji"),
            "icon_prop": obj.get("icon_prop"),
            "module_view": obj.get("module_view"),
            "cycle_view": obj.get("cycle_view"),
            "issue_views_view": obj.get("issue_views_view"),
            "page_view": obj.get("page_view"),
            "intake_view": obj.get("intake_view"),
            "is_time_tracking_enabled": obj.get("is_time_tracking_enabled"),
            "is_issue_type_enabled": obj.get("is_issue_type_enabled"),
            "guest_view_all_features": obj.get("guest_view_all_features"),
            "cover_image": obj.get("cover_image"),
            "archive_in": obj.get("archive_in"),
            "close_in": obj.get("close_in"),
            "logo_props": obj.get("logo_props"),
            "archived_at": obj.get("archived_at"),
            "timezone": obj.get("timezone"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "workspace": obj.get("workspace"),
            "default_assignee": obj.get("default_assignee"),
            "project_lead": obj.get("project_lead"),
            "cover_image_asset": obj.get("cover_image_asset"),
            "estimate": obj.get("estimate"),
            "default_state": obj.get("default_state")
        })
        return _obj


