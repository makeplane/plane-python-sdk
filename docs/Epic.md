# Epic


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**point** | **int** |  | [optional] 
**name** | **str** |  | 
**description** | **object** |  | [optional] 
**description_html** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 
**description_binary** | **bytearray** |  | [optional] [readonly] 
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
**updated_by** | **str** |  | [optional] 
**project** | **str** |  | 
**workspace** | **str** |  | 
**parent** | **str** |  | [optional] 
**state** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**type** | **str** |  | [optional] 
**assignees** | **List[str]** |  | [optional] [readonly] 
**labels** | **List[str]** |  | [optional] [readonly] 

## Example

```python
from plane.models.epic import Epic

# TODO update the JSON string below
json = "{}"
# create an instance of Epic from a JSON string
epic_instance = Epic.from_json(json)
# print the JSON string representation of the object
print(Epic.to_json())

# convert the object into a dict
epic_dict = epic_instance.to_dict()
# create an instance of Epic from a dict
epic_from_dict = Epic.from_dict(epic_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


