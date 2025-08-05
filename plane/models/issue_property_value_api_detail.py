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


from pydantic import BaseModel, Field, StrictStr, conlist

class IssuePropertyValueAPIDetail(BaseModel):
    """
    Serializer for aggregated issue property values response. This serializer handles the response format from the query_annotator method which returns property_id and values (ArrayAgg of property values).  # noqa: E501
    """
    property_id: StrictStr = Field(default=..., description="The ID of the issue property")
    values: conlist(StrictStr) = Field(default=..., description="List of aggregated property values for the given property")
    __properties = ["property_id", "values"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> IssuePropertyValueAPIDetail:
        """Create an instance of IssuePropertyValueAPIDetail from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssuePropertyValueAPIDetail:
        """Create an instance of IssuePropertyValueAPIDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssuePropertyValueAPIDetail.parse_obj(obj)

        _obj = IssuePropertyValueAPIDetail.parse_obj({
            "property_id": obj.get("property_id"),
            "values": obj.get("values")
        })
        return _obj


