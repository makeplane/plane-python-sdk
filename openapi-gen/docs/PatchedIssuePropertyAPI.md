# PatchedIssuePropertyAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**default_value** | **List[str]** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_active** | **bool** |  | [optional] 
**is_multi** | **bool** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**issue_type** | **str** |  | [optional] [readonly] 
**logo_props** | **object** |  | [optional] [readonly] 
**name** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**property_type** | [**PropertyTypeEnum**](PropertyTypeEnum.md) |  | [optional] 
**relation_type** | [**IssuePropertyAPIRelationType**](IssuePropertyAPIRelationType.md) |  | [optional] 
**settings** | **object** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**validation_rules** | **object** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue_property_api import PatchedIssuePropertyAPI

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssuePropertyAPI from a JSON string
patched_issue_property_api_instance = PatchedIssuePropertyAPI.from_json(json)
# print the JSON string representation of the object
print PatchedIssuePropertyAPI.to_json()

# convert the object into a dict
patched_issue_property_api_dict = patched_issue_property_api_instance.to_dict()
# create an instance of PatchedIssuePropertyAPI from a dict
patched_issue_property_api_from_dict = PatchedIssuePropertyAPI.from_dict(patched_issue_property_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


