# CycleCreateRequest

Serializer for creating cycles with timezone handling and date validation.  Manages cycle creation including project timezone conversion, date range validation, and UTC normalization for time-bound iteration planning and sprint management.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**start_date** | **datetime** |  | [optional] 
**end_date** | **datetime** |  | [optional] 
**owned_by** | **str** |  | 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 

## Example

```python
from plane.models.cycle_create_request import CycleCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CycleCreateRequest from a JSON string
cycle_create_request_instance = CycleCreateRequest.from_json(json)
# print the JSON string representation of the object
print CycleCreateRequest.to_json()

# convert the object into a dict
cycle_create_request_dict = cycle_create_request_instance.to_dict()
# create an instance of CycleCreateRequest from a dict
cycle_create_request_from_dict = CycleCreateRequest.from_dict(cycle_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


