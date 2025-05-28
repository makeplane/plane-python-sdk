# PatchedIssueTypeAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] [readonly] 
**level** | **int** |  | [optional] [readonly] 
**logo_props** | **object** |  | [optional] [readonly] 
**name** | **str** |  | [optional] 
**project_ids** | **List[str]** |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue_type_api import PatchedIssueTypeAPI

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueTypeAPI from a JSON string
patched_issue_type_api_instance = PatchedIssueTypeAPI.from_json(json)
# print the JSON string representation of the object
print PatchedIssueTypeAPI.to_json()

# convert the object into a dict
patched_issue_type_api_dict = patched_issue_type_api_instance.to_dict()
# create an instance of PatchedIssueTypeAPI from a dict
patched_issue_type_api_from_dict = PatchedIssueTypeAPI.from_dict(patched_issue_type_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


