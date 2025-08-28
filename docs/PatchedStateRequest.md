# PatchedStateRequest

Serializer for work item states with default state management.  Handles state creation and updates including default state validation and automatic default state switching for workflow management.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**sequence** | **float** |  | [optional] 
**group** | [**GroupEnum**](GroupEnum.md) |  | [optional] 
**is_triage** | **bool** |  | [optional] 
**default** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_state_request import PatchedStateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedStateRequest from a JSON string
patched_state_request_instance = PatchedStateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedStateRequest.to_json())

# convert the object into a dict
patched_state_request_dict = patched_state_request_instance.to_dict()
# create an instance of PatchedStateRequest from a dict
patched_state_request_from_dict = PatchedStateRequest.from_dict(patched_state_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


