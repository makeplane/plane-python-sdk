# PatchedCycleUpdateRequest

Serializer for updating cycles with enhanced ownership management.  Extends cycle creation with update-specific features including ownership assignment and modification tracking for cycle lifecycle management.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**owned_by** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 

## Example

```python
from plane.models.patched_cycle_update_request import PatchedCycleUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedCycleUpdateRequest from a JSON string
patched_cycle_update_request_instance = PatchedCycleUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedCycleUpdateRequest.to_json())

# convert the object into a dict
patched_cycle_update_request_dict = patched_cycle_update_request_instance.to_dict()
# create an instance of PatchedCycleUpdateRequest from a dict
patched_cycle_update_request_from_dict = PatchedCycleUpdateRequest.from_dict(patched_cycle_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


