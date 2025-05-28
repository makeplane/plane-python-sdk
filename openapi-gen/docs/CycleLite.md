# CycleLite


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archived_at** | **datetime** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**description** | **str** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**logo_props** | **object** |  | [optional] 
**name** | **str** |  | 
**owned_by** | **str** |  | 
**progress_snapshot** | **object** |  | [optional] 
**project** | **str** |  | 
**sort_order** | **float** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [optional] 
**version** | **int** |  | [optional] 
**view_props** | **object** |  | [optional] 
**workspace** | **str** |  | 

## Example

```python
from plane.models.cycle_lite import CycleLite

# TODO update the JSON string below
json = "{}"
# create an instance of CycleLite from a JSON string
cycle_lite_instance = CycleLite.from_json(json)
# print the JSON string representation of the object
print CycleLite.to_json()

# convert the object into a dict
cycle_lite_dict = cycle_lite_instance.to_dict()
# create an instance of CycleLite from a dict
cycle_lite_from_dict = CycleLite.from_dict(cycle_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


