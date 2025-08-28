# StateLite

Lightweight state serializer for minimal data transfer.  Provides essential state information including visual properties and grouping data optimized for UI display and filtering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**name** | **str** |  | [optional] [readonly] 
**color** | **str** |  | [optional] [readonly] 
**group** | [**GroupEnum**](GroupEnum.md) |  | [optional] [readonly] 

## Example

```python
from plane.models.state_lite import StateLite

# TODO update the JSON string below
json = "{}"
# create an instance of StateLite from a JSON string
state_lite_instance = StateLite.from_json(json)
# print the JSON string representation of the object
print(StateLite.to_json())

# convert the object into a dict
state_lite_dict = state_lite_instance.to_dict()
# create an instance of StateLite from a dict
state_lite_from_dict = StateLite.from_dict(state_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


