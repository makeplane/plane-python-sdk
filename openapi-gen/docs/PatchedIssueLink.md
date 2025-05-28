# PatchedIssueLink


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | [optional] [readonly] 
**metadata** | **object** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**title** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**url** | **str** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue_link import PatchedIssueLink

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueLink from a JSON string
patched_issue_link_instance = PatchedIssueLink.from_json(json)
# print the JSON string representation of the object
print PatchedIssueLink.to_json()

# convert the object into a dict
patched_issue_link_dict = patched_issue_link_instance.to_dict()
# create an instance of PatchedIssueLink from a dict
patched_issue_link_from_dict = PatchedIssueLink.from_dict(patched_issue_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


