# CreateStateRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | State name | [optional] 
**description** | **str** | State description | [optional] 
**color** | **str** | State color | [optional] 
**group** | **str** | State group | [optional] 
**default** | **bool** | Default state | [optional] 

## Example

```python
from plane.models.create_state_request import CreateStateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateStateRequest from a JSON string
create_state_request_instance = CreateStateRequest.from_json(json)
# print the JSON string representation of the object
print CreateStateRequest.to_json()

# convert the object into a dict
create_state_request_dict = create_state_request_instance.to_dict()
# create an instance of CreateStateRequest from a dict
create_state_request_from_dict = CreateStateRequest.from_dict(create_state_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


