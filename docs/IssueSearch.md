# IssueSearch

Search results for work items.  Provides list of issues with their identifiers, names, and project context.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | [**List[IssueSearchItem]**](IssueSearchItem.md) |  | 

## Example

```python
from plane.models.issue_search import IssueSearch

# TODO update the JSON string below
json = "{}"
# create an instance of IssueSearch from a JSON string
issue_search_instance = IssueSearch.from_json(json)
# print the JSON string representation of the object
print IssueSearch.to_json()

# convert the object into a dict
issue_search_dict = issue_search_instance.to_dict()
# create an instance of IssueSearch from a dict
issue_search_from_dict = IssueSearch.from_dict(issue_search_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


