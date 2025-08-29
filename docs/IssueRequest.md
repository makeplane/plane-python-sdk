# IssueRequest

Comprehensive work item serializer with full relationship management.  Handles complete work item lifecycle including assignees, labels, validation, and related model updates. Supports dynamic field expansion and HTML content processing.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignees** | **List[str]** |  | [optional] 
**labels** | **List[str]** |  | [optional] 
**type_id** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**point** | **int** |  | [optional] 
**name** | **str** |  | 
**description_html** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 
**start_date** | **date** |  | [optional] 
**target_date** | **date** |  | [optional] 
**sequence_id** | **int** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 
**archived_at** | **date** |  | [optional] 
**is_draft** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**state** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_request import IssueRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRequest from a JSON string
issue_request_instance = IssueRequest.from_json(json)
# print the JSON string representation of the object
print(IssueRequest.to_json())

# convert the object into a dict
issue_request_dict = issue_request_instance.to_dict()
# create an instance of IssueRequest from a dict
issue_request_from_dict = IssueRequest.from_dict(issue_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


