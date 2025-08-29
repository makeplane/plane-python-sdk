# PaginatedIssueActivityResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**grouped_by** | **str** |  | 
**sub_grouped_by** | **str** |  | 
**total_count** | **int** |  | 
**next_cursor** | **str** |  | 
**prev_cursor** | **str** |  | 
**next_page_results** | **bool** |  | 
**prev_page_results** | **bool** |  | 
**count** | **int** |  | 
**total_pages** | **int** |  | 
**total_results** | **int** |  | 
**extra_stats** | **str** |  | 
**results** | [**List[IssueActivity]**](IssueActivity.md) |  | 

## Example

```python
from plane.models.paginated_issue_activity_response import PaginatedIssueActivityResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedIssueActivityResponse from a JSON string
paginated_issue_activity_response_instance = PaginatedIssueActivityResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedIssueActivityResponse.to_json())

# convert the object into a dict
paginated_issue_activity_response_dict = paginated_issue_activity_response_instance.to_dict()
# create an instance of PaginatedIssueActivityResponse from a dict
paginated_issue_activity_response_from_dict = PaginatedIssueActivityResponse.from_dict(paginated_issue_activity_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


