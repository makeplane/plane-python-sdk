# IssueExpand

Extended work item serializer with full relationship expansion.  Provides work items with expanded related data including cycles, modules, labels, assignees, and states for comprehensive data representation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**cycle** | [**CycleLite**](CycleLite.md) |  | [optional] [readonly] 
**module** | [**ModuleLite**](ModuleLite.md) |  | [optional] [readonly] 
**labels** | **str** |  | [optional] [readonly] 
**assignees** | **str** |  | [optional] [readonly] 
**state** | [**StateLite**](StateLite.md) |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
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
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**parent** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_expand import IssueExpand

# TODO update the JSON string below
json = "{}"
# create an instance of IssueExpand from a JSON string
issue_expand_instance = IssueExpand.from_json(json)
# print the JSON string representation of the object
print(IssueExpand.to_json())

# convert the object into a dict
issue_expand_dict = issue_expand_instance.to_dict()
# create an instance of IssueExpand from a dict
issue_expand_from_dict = IssueExpand.from_dict(issue_expand_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


