# Issue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **date** |  | [optional] 
**assignees** | **List[str]** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**description_binary** | **bytearray** |  | [readonly] 
**description_html** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_draft** | **bool** |  | [optional] 
**labels** | **List[str]** |  | [optional] 
**name** | **str** |  | 
**parent** | **str** |  | [optional] 
**point** | **int** |  | [optional] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 
**project** | **str** |  | [readonly] 
**sequence_id** | **int** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**state** | **str** |  | [optional] 
**target_date** | **date** |  | [optional] 
**type** | **str** |  | [optional] 
**type_id** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue import Issue

# TODO update the JSON string below
json = "{}"
# create an instance of Issue from a JSON string
issue_instance = Issue.from_json(json)
# print the JSON string representation of the object
print Issue.to_json()

# convert the object into a dict
issue_dict = issue_instance.to_dict()
# create an instance of Issue from a dict
issue_from_dict = Issue.from_dict(issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


