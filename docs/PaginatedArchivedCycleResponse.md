# PaginatedArchivedCycleResponse


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
**results** | [**List[Cycle]**](Cycle.md) |  | 

## Example

```python
from plane.models.paginated_archived_cycle_response import PaginatedArchivedCycleResponse

# TODO update the JSON string below
json = "{}"
# create an instance of PaginatedArchivedCycleResponse from a JSON string
paginated_archived_cycle_response_instance = PaginatedArchivedCycleResponse.from_json(json)
# print the JSON string representation of the object
print(PaginatedArchivedCycleResponse.to_json())

# convert the object into a dict
paginated_archived_cycle_response_dict = paginated_archived_cycle_response_instance.to_dict()
# create an instance of PaginatedArchivedCycleResponse from a dict
paginated_archived_cycle_response_from_dict = PaginatedArchivedCycleResponse.from_dict(paginated_archived_cycle_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


