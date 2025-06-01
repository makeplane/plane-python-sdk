# IssueLink


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**title** | **str** |  | [optional] 
**url** | **str** |  | 
**metadata** | **object** |  | [optional] 
**created_by** | **str** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 
**issue** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_link import IssueLink

# TODO update the JSON string below
json = "{}"
# create an instance of IssueLink from a JSON string
issue_link_instance = IssueLink.from_json(json)
# print the JSON string representation of the object
print IssueLink.to_json()

# convert the object into a dict
issue_link_dict = issue_link_instance.to_dict()
# create an instance of IssueLink from a dict
issue_link_from_dict = IssueLink.from_dict(issue_link_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


