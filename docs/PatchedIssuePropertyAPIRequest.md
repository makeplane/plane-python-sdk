# PatchedIssuePropertyAPIRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relation_type** | [**RelationTypeEnum**](RelationTypeEnum.md) |  | [optional] 
**display_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**property_type** | [**PropertyTypeEnum**](PropertyTypeEnum.md) |  | [optional] 
**is_required** | **bool** |  | [optional] 
**default_value** | **List[str]** |  | [optional] 
**settings** | **object** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**is_multi** | **bool** |  | [optional] 
**validation_rules** | **object** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_property_api_request import PatchedIssuePropertyAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssuePropertyAPIRequest from a JSON string
patched_issue_property_api_request_instance = PatchedIssuePropertyAPIRequest.from_json(json)
# print the JSON string representation of the object
print PatchedIssuePropertyAPIRequest.to_json()

# convert the object into a dict
patched_issue_property_api_request_dict = patched_issue_property_api_request_instance.to_dict()
# create an instance of PatchedIssuePropertyAPIRequest from a dict
patched_issue_property_api_request_from_dict = PatchedIssuePropertyAPIRequest.from_dict(patched_issue_property_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


