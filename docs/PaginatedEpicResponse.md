# PaginatedEpicResponse


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
**results** | [**List[Epic]**](Epic.md) |  | 

## Example

```python
from plane.models.paginated_epic_response import PaginatedEpicResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedEpicResponse from a JSON string
paginated_epic_response_instance = PaginatedEpicResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedEpicResponse.to_json())

# convert the object into a dict
paginated_epic_response_dict = paginated_epic_response_instance.to_dict()
# create an instance of PaginatedEpicResponse from a dict
paginated_epic_response_from_dict = PaginatedEpicResponse.from_dict(paginated_epic_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


