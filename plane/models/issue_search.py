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



from pydantic import BaseModel, Field, StrictStr

class IssueSearch(BaseModel):
    """
    Serializer for work item search result data formatting.  Provides standardized search result structure including work item identifiers, project context, and workspace information for search API responses.  # noqa: E501
    """
    id: StrictStr = Field(default=..., description="Issue ID")
    name: StrictStr = Field(default=..., description="Issue name")
    sequence_id: StrictStr = Field(default=..., description="Issue sequence ID")
    project__identifier: StrictStr = Field(default=..., description="Project identifier")
    project_id: StrictStr = Field(default=..., description="Project ID")
    workspace__slug: StrictStr = Field(default=..., description="Workspace slug")
    __properties = ["id", "name", "sequence_id", "project__identifier", "project_id", "workspace__slug"]

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
    def from_json(cls, json_str: str) -> IssueSearch:
        """Create an instance of IssueSearch from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IssueSearch:
        """Create an instance of IssueSearch from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IssueSearch.parse_obj(obj)

        _obj = IssueSearch.parse_obj({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "sequence_id": obj.get("sequence_id"),
            "project__identifier": obj.get("project__identifier"),
            "project_id": obj.get("project_id"),
            "workspace__slug": obj.get("workspace__slug")
        })
        return _obj


