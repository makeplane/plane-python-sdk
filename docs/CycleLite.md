# CycleLite

Lightweight cycle serializer for minimal data transfer.  Provides essential cycle information without computed metrics, optimized for list views and reference lookups.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
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
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 
**project** | **str** |  | 
**workspace** | **str** |  | 
**owned_by** | **str** |  | 

## Example

```python
from plane.models.cycle_lite import CycleLite

# TODO update the JSON string below
json = "{}"
# create an instance of CycleLite from a JSON string
cycle_lite_instance = CycleLite.from_json(json)
# print the JSON string representation of the object
print(CycleLite.to_json())

# convert the object into a dict
cycle_lite_dict = cycle_lite_instance.to_dict()
# create an instance of CycleLite from a dict
cycle_lite_from_dict = CycleLite.from_dict(cycle_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


