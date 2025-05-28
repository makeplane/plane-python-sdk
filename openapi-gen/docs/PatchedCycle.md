# PatchedCycle


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**backlog_issues** | **int** |  | [optional] [readonly] 
**cancelled_issues** | **int** |  | [optional] [readonly] 
**completed_estimates** | **float** |  | [optional] [readonly] 
**completed_issues** | **int** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**logo_props** | **object** |  | [optional] 
**name** | **str** |  | [optional] 
**owned_by** | **str** |  | [optional] [readonly] 
**progress_snapshot** | **object** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**started_estimates** | **float** |  | [optional] [readonly] 
**started_issues** | **int** |  | [optional] [readonly] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**total_estimates** | **float** |  | [optional] [readonly] 
**total_issues** | **int** |  | [optional] [readonly] 
**unstarted_issues** | **int** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**version** | **int** |  | [optional] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_cycle import PatchedCycle

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedCycle from a JSON string
patched_cycle_instance = PatchedCycle.from_json(json)
# print the JSON string representation of the object
print PatchedCycle.to_json()

# convert the object into a dict
patched_cycle_dict = patched_cycle_instance.to_dict()
# create an instance of PatchedCycle from a dict
patched_cycle_from_dict = PatchedCycle.from_dict(patched_cycle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


