# PatchedState


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**default** | **bool** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**group** | [**GroupEnum**](GroupEnum.md) |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_triage** | **bool** |  | [optional] 
**name** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**sequence** | **float** |  | [optional] 
**slug** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_state import PatchedState

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedState from a JSON string
patched_state_instance = PatchedState.from_json(json)
# print the JSON string representation of the object
print PatchedState.to_json()

# convert the object into a dict
patched_state_dict = patched_state_instance.to_dict()
# create an instance of PatchedState from a dict
patched_state_from_dict = PatchedState.from_dict(patched_state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


