# PaginatedProjectResponse


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
**results** | [**List[Project]**](Project.md) |  | 

## Example

```python
from plane.models.paginated_project_response import PaginatedProjectResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedProjectResponse from a JSON string
paginated_project_response_instance = PaginatedProjectResponse.from_json(json)
# print the JSON string representation of the object
print PaginatedProjectResponse.to_json()

# convert the object into a dict
paginated_project_response_dict = paginated_project_response_instance.to_dict()
# create an instance of PaginatedProjectResponse from a dict
paginated_project_response_from_dict = PaginatedProjectResponse.from_dict(paginated_project_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


