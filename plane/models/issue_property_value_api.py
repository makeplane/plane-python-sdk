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
from typing import Set
from typing_extensions import Self

class IssuePropertyValueAPI(BaseModel):
    """
    IssuePropertyValueAPI
    """ # noqa: E501
    id: Optional[StrictStr] = None
    deleted_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    value_text: Optional[StrictStr] = None
    value_boolean: Optional[StrictBool] = None
    value_decimal: Optional[Union[StrictFloat, StrictInt]] = None
    value_datetime: Optional[datetime] = None
    value_uuid: Optional[StrictStr] = None
    external_source: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    external_id: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    created_by: Optional[StrictStr] = None
    updated_by: Optional[StrictStr] = None
    workspace: Optional[StrictStr] = None
    project: Optional[StrictStr] = None
    issue: StrictStr
    var_property: StrictStr = Field(alias="property")
    value_option: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["id", "deleted_at", "created_at", "updated_at", "value_text", "value_boolean", "value_decimal", "value_datetime", "value_uuid", "external_source", "external_id", "created_by", "updated_by", "workspace", "project", "issue", "property", "value_option"]

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
        """Create an instance of IssuePropertyValueAPI from a JSON string"""
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
        """
        excluded_fields: Set[str] = set([
            "id",
            "deleted_at",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "workspace",
            "project",
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

        # set to None if value_datetime (nullable) is None
        # and model_fields_set contains the field
        if self.value_datetime is None and "value_datetime" in self.model_fields_set:
            _dict['value_datetime'] = None

        # set to None if value_uuid (nullable) is None
        # and model_fields_set contains the field
        if self.value_uuid is None and "value_uuid" in self.model_fields_set:
            _dict['value_uuid'] = None

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

        # set to None if project (nullable) is None
        # and model_fields_set contains the field
        if self.project is None and "project" in self.model_fields_set:
            _dict['project'] = None

        # set to None if value_option (nullable) is None
        # and model_fields_set contains the field
        if self.value_option is None and "value_option" in self.model_fields_set:
            _dict['value_option'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IssuePropertyValueAPI from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "deleted_at": obj.get("deleted_at"),
            "created_at": obj.get("created_at"),
            "updated_at": obj.get("updated_at"),
            "value_text": obj.get("value_text"),
            "value_boolean": obj.get("value_boolean"),
            "value_decimal": obj.get("value_decimal"),
            "value_datetime": obj.get("value_datetime"),
            "value_uuid": obj.get("value_uuid"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "created_by": obj.get("created_by"),
            "updated_by": obj.get("updated_by"),
            "workspace": obj.get("workspace"),
            "project": obj.get("project"),
            "issue": obj.get("issue"),
            "property": obj.get("property"),
            "value_option": obj.get("value_option")
        })
        return _obj


