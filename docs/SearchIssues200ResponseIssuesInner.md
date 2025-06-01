# SearchIssues200ResponseIssuesInner


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Issue name | [optional] 
**id** | **str** | Issue ID | [optional] 
**sequence_id** | **str** | Issue sequence ID | [optional] 
**project__identifier** | **str** | Project identifier | [optional] 
**project_id** | **str** | Project ID | [optional] 
**workspace__slug** | **str** | Workspace slug | [optional] 

## Example

```python
from plane.models.search_issues200_response_issues_inner import SearchIssues200ResponseIssuesInner

# TODO update the JSON string below
json = "{}"
# create an instance of SearchIssues200ResponseIssuesInner from a JSON string
search_issues200_response_issues_inner_instance = SearchIssues200ResponseIssuesInner.from_json(json)
# print the JSON string representation of the object
print SearchIssues200ResponseIssuesInner.to_json()

# convert the object into a dict
search_issues200_response_issues_inner_dict = search_issues200_response_issues_inner_instance.to_dict()
# create an instance of SearchIssues200ResponseIssuesInner from a dict
search_issues200_response_issues_inner_from_dict = SearchIssues200ResponseIssuesInner.from_dict(search_issues200_response_issues_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


