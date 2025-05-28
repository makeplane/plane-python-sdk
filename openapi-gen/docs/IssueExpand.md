# IssueExpand


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **date** |  | [optional] 
**assignees** | [**List[UserLite]**](UserLite.md) |  | [readonly] 
**completed_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**cycle** | [**CycleLite**](CycleLite.md) |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**description** | **object** |  | [optional] 
**description_binary** | **bytearray** |  | [readonly] 
**description_html** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 
**estimate_point** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_draft** | **bool** |  | [optional] 
**labels** | [**List[LabelLite]**](LabelLite.md) |  | [readonly] 
**module** | [**ModuleLite**](ModuleLite.md) |  | [readonly] 
**name** | **str** |  | 
**parent** | **str** |  | [optional] 
**point** | **int** |  | [optional] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 
**project** | **str** |  | [readonly] 
**sequence_id** | **int** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**state** | [**StateLite**](StateLite.md) |  | [readonly] 
**target_date** | **date** |  | [optional] 
**type** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_expand import IssueExpand

# TODO update the JSON string below
json = "{}"
# create an instance of IssueExpand from a JSON string
issue_expand_instance = IssueExpand.from_json(json)
# print the JSON string representation of the object
print IssueExpand.to_json()

# convert the object into a dict
issue_expand_dict = issue_expand_instance.to_dict()
# create an instance of IssueExpand from a dict
issue_expand_from_dict = IssueExpand.from_dict(issue_expand_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


