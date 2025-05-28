# IssueLink


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**id** | **str** |  | [readonly] 
**issue** | **str** |  | [readonly] 
**metadata** | **object** |  | [optional] 
**project** | **str** |  | [readonly] 
**title** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**url** | **str** |  | 
**workspace** | **str** |  | [readonly] 

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


