# Module


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**backlog_issues** | **int** |  | [readonly] 
**cancelled_issues** | **int** |  | [readonly] 
**completed_issues** | **int** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**description_html** | **object** |  | [optional] 
**description_text** | **object** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**lead** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**members** | **List[str]** |  | [optional] 
**name** | **str** |  | 
**project** | **str** |  | [readonly] 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**started_issues** | **int** |  | [readonly] 
**status** | [**StatusA3dEnum**](StatusA3dEnum.md) |  | [optional] 
**target_date** | **date** |  | [optional] 
**total_issues** | **int** |  | [readonly] 
**unstarted_issues** | **int** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | [readonly] 

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


