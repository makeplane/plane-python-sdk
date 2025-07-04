# ModuleLite

Lightweight module serializer for minimal data transfer.  Provides essential module information without computed metrics, optimized for list views and reference lookups.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | 
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
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 
**project** | **str** |  | 
**workspace** | **str** |  | 
**lead** | **str** |  | [optional] 
**members** | **List[str]** |  | [optional] [readonly] 

## Example

```python
from plane.models.module_lite import ModuleLite

# TODO update the JSON string below
json = "{}"
# create an instance of ModuleLite from a JSON string
module_lite_instance = ModuleLite.from_json(json)
# print the JSON string representation of the object
print ModuleLite.to_json()

# convert the object into a dict
module_lite_dict = module_lite_instance.to_dict()
# create an instance of ModuleLite from a dict
module_lite_from_dict = ModuleLite.from_dict(module_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


