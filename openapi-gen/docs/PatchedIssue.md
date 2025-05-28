# PatchedIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **date** |  | [optional] 
**assignees** | **List[str]** |  | [optional] 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**description_binary** | **bytearray** |  | [optional] [readonly] 
**description_html** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_draft** | **bool** |  | [optional] 
**labels** | **List[str]** |  | [optional] 
**name** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**point** | **int** |  | [optional] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**sequence_id** | **int** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**state** | **str** |  | [optional] 
**target_date** | **date** |  | [optional] 
**type** | **str** |  | [optional] 
**type_id** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue import PatchedIssue

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssue from a JSON string
patched_issue_instance = PatchedIssue.from_json(json)
# print the JSON string representation of the object
print PatchedIssue.to_json()

# convert the object into a dict
patched_issue_dict = patched_issue_instance.to_dict()
# create an instance of PatchedIssue from a dict
patched_issue_from_dict = PatchedIssue.from_dict(patched_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


