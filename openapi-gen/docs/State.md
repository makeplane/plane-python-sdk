# State


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** |  | 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**default** | **bool** |  | [optional] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**group** | [**GroupEnum**](GroupEnum.md) |  | [optional] 
**id** | **str** |  | [readonly] 
**is_triage** | **bool** |  | [optional] 
**name** | **str** |  | 
**project** | **str** |  | [readonly] 
**sequence** | **float** |  | [optional] 
**slug** | **str** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.state import State

# TODO update the JSON string below
json = "{}"
# create an instance of State from a JSON string
state_instance = State.from_json(json)
# print the JSON string representation of the object
print State.to_json()

# convert the object into a dict
state_dict = state_instance.to_dict()
# create an instance of State from a dict
state_from_dict = State.from_dict(state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


