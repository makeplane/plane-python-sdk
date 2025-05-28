# Cycle


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**backlog_issues** | **int** |  | [readonly] 
**cancelled_issues** | **int** |  | [readonly] 
**completed_estimates** | **float** |  | [readonly] 
**completed_issues** | **int** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**logo_props** | **object** |  | [optional] 
**name** | **str** |  | 
**owned_by** | **str** |  | [readonly] 
**progress_snapshot** | **object** |  | [optional] 
**project** | **str** |  | [readonly] 
**sort_order** | **float** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**started_estimates** | **float** |  | [readonly] 
**started_issues** | **int** |  | [readonly] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**total_estimates** | **float** |  | [readonly] 
**total_issues** | **int** |  | [readonly] 
**unstarted_issues** | **int** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**version** | **int** |  | [optional] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.cycle import Cycle

# TODO update the JSON string below
json = "{}"
# create an instance of Cycle from a JSON string
cycle_instance = Cycle.from_json(json)
# print the JSON string representation of the object
print Cycle.to_json()

# convert the object into a dict
cycle_dict = cycle_instance.to_dict()
# create an instance of Cycle from a dict
cycle_from_dict = Cycle.from_dict(cycle_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


