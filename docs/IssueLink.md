# IssueLink

Full serializer for work item external links.  Provides complete link information including metadata and timestamps for managing external resource associations with work items.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**title** | **str** |  | [optional] 
**url** | **str** |  | 
**metadata** | **object** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.issue_link import IssueLink

# TODO update the JSON string below
json = "{}"
# create an instance of IssueLink from a JSON string
issue_link_instance = IssueLink.from_json(json)
# print the JSON string representation of the object
print(IssueLink.to_json())

# convert the object into a dict
issue_link_dict = issue_link_instance.to_dict()
# create an instance of IssueLink from a dict
issue_link_from_dict = IssueLink.from_dict(issue_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


