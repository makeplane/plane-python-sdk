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

from datetime import date
from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from plane.models.page_create_api_access_enum import PageCreateAPIAccessEnum
from typing import Set
from typing_extensions import Self

class PageCreateAPIRequest(BaseModel):
    """
    PageCreateAPIRequest
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True)]
    access: Optional[PageCreateAPIAccessEnum] = None
    color: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    is_locked: Optional[StrictBool] = None
    archived_at: Optional[date] = None
    view_props: Optional[Any] = None
    logo_props: Optional[Any] = None
    external_id: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    external_source: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    description_html: Annotated[str, Field(min_length=1, strict=True)]
    __properties: ClassVar[List[str]] = ["name", "access", "color", "is_locked", "archived_at", "view_props", "logo_props", "external_id", "external_source", "description_html"]

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
        """Create an instance of PageCreateAPIRequest from a JSON string"""
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
        # set to None if archived_at (nullable) is None
        # and model_fields_set contains the field
        if self.archived_at is None and "archived_at" in self.model_fields_set:
            _dict['archived_at'] = None

        # set to None if view_props (nullable) is None
        # and model_fields_set contains the field
        if self.view_props is None and "view_props" in self.model_fields_set:
            _dict['view_props'] = None

        # set to None if logo_props (nullable) is None
        # and model_fields_set contains the field
        if self.logo_props is None and "logo_props" in self.model_fields_set:
            _dict['logo_props'] = None

        # set to None if external_id (nullable) is None
        # and model_fields_set contains the field
        if self.external_id is None and "external_id" in self.model_fields_set:
            _dict['external_id'] = None

        # set to None if external_source (nullable) is None
        # and model_fields_set contains the field
        if self.external_source is None and "external_source" in self.model_fields_set:
            _dict['external_source'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PageCreateAPIRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "access": obj.get("access"),
            "color": obj.get("color"),
            "is_locked": obj.get("is_locked"),
            "archived_at": obj.get("archived_at"),
            "view_props": obj.get("view_props"),
            "logo_props": obj.get("logo_props"),
            "external_id": obj.get("external_id"),
            "external_source": obj.get("external_source"),
            "description_html": obj.get("description_html")
        })
        return _obj


