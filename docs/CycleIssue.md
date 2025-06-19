# CycleIssue

Serializer for cycle-issue relationships with sub-issue counting.  Manages the association between cycles and work items, including hierarchical issue tracking for nested work item structures.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**sub_issues_count** | **int** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | 
**cycle** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.cycle_issue import CycleIssue

# TODO update the JSON string below
json = "{}"
# create an instance of CycleIssue from a JSON string
cycle_issue_instance = CycleIssue.from_json(json)
# print the JSON string representation of the object
print CycleIssue.to_json()

# convert the object into a dict
cycle_issue_dict = cycle_issue_instance.to_dict()
# create an instance of CycleIssue from a dict
cycle_issue_from_dict = CycleIssue.from_dict(cycle_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


