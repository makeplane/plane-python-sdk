# IssueSearch

Serializer for work item search result data formatting.  Provides standardized search result structure including work item identifiers, project context, and workspace information for search API responses.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | [**List[IssueSearchItem]**](IssueSearchItem.md) | Array of search result issues | 

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


