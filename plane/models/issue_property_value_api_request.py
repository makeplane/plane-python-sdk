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

class IssuePropertyValueAPIRequest(BaseModel):
    """
    IssuePropertyValueAPIRequest
    """ # noqa: E501
    value_text: Optional[StrictStr] = None
    value_boolean: Optional[StrictBool] = None
    value_decimal: Optional[Union[StrictFloat, StrictInt]] = None
    value_datetime: Optional[datetime] = None
    value_uuid: Optional[StrictStr] = None
    external_source: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    external_id: Optional[Annotated[str, Field(strict=True, max_length=255)]] = None
    issue: StrictStr
    var_property: StrictStr = Field(alias="property")
    value_option: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = ["value_text", "value_boolean", "value_decimal", "value_datetime", "value_uuid", "external_source", "external_id", "issue", "property", "value_option"]

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
        """Create an instance of IssuePropertyValueAPIRequest from a JSON string"""
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

        # set to None if value_option (nullable) is None
        # and model_fields_set contains the field
        if self.value_option is None and "value_option" in self.model_fields_set:
            _dict['value_option'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IssuePropertyValueAPIRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "value_text": obj.get("value_text"),
            "value_boolean": obj.get("value_boolean"),
            "value_decimal": obj.get("value_decimal"),
            "value_datetime": obj.get("value_datetime"),
            "value_uuid": obj.get("value_uuid"),
            "external_source": obj.get("external_source"),
            "external_id": obj.get("external_id"),
            "issue": obj.get("issue"),
            "property": obj.get("property"),
            "value_option": obj.get("value_option")
        })
        return _obj


