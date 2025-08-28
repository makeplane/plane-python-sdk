# PaginatedIntakeIssueResponse


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
**results** | [**List[IntakeIssue]**](IntakeIssue.md) |  | 

## Example

```python
from plane.models.paginated_intake_issue_response import PaginatedIntakeIssueResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedIntakeIssueResponse from a JSON string
paginated_intake_issue_response_instance = PaginatedIntakeIssueResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedIntakeIssueResponse.to_json())

# convert the object into a dict
paginated_intake_issue_response_dict = paginated_intake_issue_response_instance.to_dict()
# create an instance of PaginatedIntakeIssueResponse from a dict
paginated_intake_issue_response_from_dict = PaginatedIntakeIssueResponse.from_dict(paginated_intake_issue_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


