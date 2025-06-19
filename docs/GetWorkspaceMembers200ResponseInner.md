# GetWorkspaceMembers200ResponseInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**first_name** | **str** |  | [optional] [readonly] 
**last_name** | **str** |  | [optional] [readonly] 
**email** | **str** |  | [optional] [readonly] 
**avatar** | **str** |  | [optional] [readonly] 
**avatar_url** | **str** | Avatar URL | [optional] [readonly] 
**display_name** | **str** |  | [optional] [readonly] 
**role** | **int** | Member role in the workspace | [optional] 

## Example

```python
from plane.models.get_workspace_members200_response_inner import GetWorkspaceMembers200ResponseInner

# TODO update the JSON string below
json = "{}"
# create an instance of GetWorkspaceMembers200ResponseInner from a JSON string
get_workspace_members200_response_inner_instance = GetWorkspaceMembers200ResponseInner.from_json(json)
# print the JSON string representation of the object
print GetWorkspaceMembers200ResponseInner.to_json()

# convert the object into a dict
get_workspace_members200_response_inner_dict = get_workspace_members200_response_inner_instance.to_dict()
# create an instance of GetWorkspaceMembers200ResponseInner from a dict
get_workspace_members200_response_inner_from_dict = GetWorkspaceMembers200ResponseInner.from_dict(get_workspace_members200_response_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


