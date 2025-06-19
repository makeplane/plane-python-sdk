# IssueTypeAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**project_ids** | **List[str]** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] [readonly] 
**is_epic** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] [readonly] 
**is_active** | **bool** |  | [optional] 
**level** | **float** |  | [optional] [readonly] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.issue_type_api import IssueTypeAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssueTypeAPI from a JSON string
issue_type_api_instance = IssueTypeAPI.from_json(json)
# print the JSON string representation of the object
print IssueTypeAPI.to_json()

# convert the object into a dict
issue_type_api_dict = issue_type_api_instance.to_dict()
# create an instance of IssueTypeAPI from a dict
issue_type_api_from_dict = IssueTypeAPI.from_dict(issue_type_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


