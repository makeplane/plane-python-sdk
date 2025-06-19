# Cycle

Cycle serializer with comprehensive project metrics and time tracking.  Provides cycle details including work item counts by status, progress estimates, and time-bound iteration data for project management and sprint planning.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**total_issues** | **int** |  | [optional] [readonly] 
**cancelled_issues** | **int** |  | [optional] [readonly] 
**completed_issues** | **int** |  | [optional] [readonly] 
**started_issues** | **int** |  | [optional] [readonly] 
**unstarted_issues** | **int** |  | [optional] [readonly] 
**backlog_issues** | **int** |  | [optional] [readonly] 
**total_estimates** | **float** |  | [optional] [readonly] 
**completed_estimates** | **float** |  | [optional] [readonly] 
**started_estimates** | **float** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**view_props** | **object** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**progress_snapshot** | **object** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**version** | **int** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**owned_by** | **str** |  | [optional] [readonly] 

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


