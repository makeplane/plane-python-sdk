# ModuleLite


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | 
**description** | **str** |  | [optional] 
**description_html** | **object** |  | [optional] 
**description_text** | **object** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**lead** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**members** | **List[str]** |  | [readonly] 
**name** | **str** |  | 
**project** | **str** |  | 
**sort_order** | **float** |  | [optional] 
**start_date** | **date** |  | [optional] 
**status** | [**StatusA3dEnum**](StatusA3dEnum.md) |  | [optional] 
**target_date** | **date** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [optional] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | 

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


