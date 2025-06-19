# Module

Comprehensive module serializer with work item metrics and member management.  Provides complete module data including work item counts by status, member relationships, and progress tracking for feature-based project organization.

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
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**description_text** | **object** |  | [optional] 
**description_html** | **object** |  | [optional] 
**start_date** | **date** |  | [optional] 
**target_date** | **date** |  | [optional] 
**status** | [**ModuleStatusEnum**](ModuleStatusEnum.md) |  | [optional] 
**view_props** | **object** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**lead** | **str** |  | [optional] 

## Example

```python
from plane.models.module import Module

# TODO update the JSON string below
json = "{}"
# create an instance of Module from a JSON string
module_instance = Module.from_json(json)
# print the JSON string representation of the object
print Module.to_json()

# convert the object into a dict
module_dict = module_instance.to_dict()
# create an instance of Module from a dict
module_from_dict = Module.from_dict(module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


