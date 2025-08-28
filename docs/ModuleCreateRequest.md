# ModuleCreateRequest

Serializer for creating modules with member validation and date checking.  Handles module creation including member assignment validation, date range verification, and duplicate name prevention for feature-based project organization setup.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**start_date** | **date** |  | [optional] 
**target_date** | **date** |  | [optional] 
**status** | [**ModuleStatusEnum**](ModuleStatusEnum.md) |  | [optional] 
**lead** | **str** |  | [optional] 
**members** | **List[str]** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.module_create_request import ModuleCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModuleCreateRequest from a JSON string
module_create_request_instance = ModuleCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ModuleCreateRequest.to_json())

# convert the object into a dict
module_create_request_dict = module_create_request_instance.to_dict()
# create an instance of ModuleCreateRequest from a dict
module_create_request_from_dict = ModuleCreateRequest.from_dict(module_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


