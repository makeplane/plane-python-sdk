# CreateCycleRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Cycle Name | 
**description** | **str** | Cycle Description | [optional] 
**start_date** | **datetime** | Start Date | [optional] 
**end_date** | **datetime** | End Date | [optional] 

## Example

```python
from plane.models.create_cycle_request import CreateCycleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateCycleRequest from a JSON string
create_cycle_request_instance = CreateCycleRequest.from_json(json)
# print the JSON string representation of the object
print CreateCycleRequest.to_json()

# convert the object into a dict
create_cycle_request_dict = create_cycle_request_instance.to_dict()
# create an instance of CreateCycleRequest from a dict
create_cycle_request_from_dict = CreateCycleRequest.from_dict(create_cycle_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


