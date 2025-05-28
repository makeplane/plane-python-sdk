# IssueTypeAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [readonly] 
**level** | **int** |  | [readonly] 
**logo_props** | **object** |  | [readonly] 
**name** | **str** |  | 
**project_ids** | **List[str]** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

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


