# PatchedModuleUpdateRequest

Serializer for updating modules with enhanced validation and member management.  Extends module creation with update-specific validations including member reassignment, name conflict checking, and relationship management for module modifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
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
from plane.models.patched_module_update_request import PatchedModuleUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedModuleUpdateRequest from a JSON string
patched_module_update_request_instance = PatchedModuleUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedModuleUpdateRequest.to_json())

# convert the object into a dict
patched_module_update_request_dict = patched_module_update_request_instance.to_dict()
# create an instance of PatchedModuleUpdateRequest from a dict
patched_module_update_request_from_dict = PatchedModuleUpdateRequest.from_dict(patched_module_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


