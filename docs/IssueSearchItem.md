# IssueSearchItem

Individual issue component for search results.  Provides standardized search result structure including work item identifiers, project context, and workspace information for search API responses.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Issue ID | 
**name** | **str** | Issue name | 
**sequence_id** | **str** | Issue sequence ID | 
**project__identifier** | **str** | Project identifier | 
**project_id** | **str** | Project ID | 
**workspace__slug** | **str** | Workspace slug | 

## Example

```python
from plane.models.issue_search_item import IssueSearchItem

# TODO update the JSON string below
json = "{}"
# create an instance of IssueSearchItem from a JSON string
issue_search_item_instance = IssueSearchItem.from_json(json)
# print the JSON string representation of the object
print IssueSearchItem.to_json()

# convert the object into a dict
issue_search_item_dict = issue_search_item_instance.to_dict()
# create an instance of IssueSearchItem from a dict
issue_search_item_from_dict = IssueSearchItem.from_dict(issue_search_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


