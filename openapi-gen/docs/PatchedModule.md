# PatchedModule


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**backlog_issues** | **int** |  | [optional] [readonly] 
**cancelled_issues** | **int** |  | [optional] [readonly] 
**completed_issues** | **int** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**description_html** | **object** |  | [optional] 
**description_text** | **object** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**lead** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**members** | **List[str]** |  | [optional] 
**name** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**started_issues** | **int** |  | [optional] [readonly] 
**status** | [**StatusA3dEnum**](StatusA3dEnum.md) |  | [optional] 
**target_date** | **date** |  | [optional] 
**total_issues** | **int** |  | [optional] [readonly] 
**unstarted_issues** | **int** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_module import PatchedModule

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedModule from a JSON string
patched_module_instance = PatchedModule.from_json(json)
# print the JSON string representation of the object
print PatchedModule.to_json()

# convert the object into a dict
patched_module_dict = patched_module_instance.to_dict()
# create an instance of PatchedModule from a dict
patched_module_from_dict = PatchedModule.from_dict(patched_module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


