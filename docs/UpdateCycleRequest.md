# UpdateCycleRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Cycle Name | [optional] 
**description** | **str** | Cycle Description | [optional] 
**start_date** | **datetime** | Start Date | [optional] 
**end_date** | **datetime** | End Date | [optional] 

## Example

```python
from plane.models.update_cycle_request import UpdateCycleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCycleRequest from a JSON string
update_cycle_request_instance = UpdateCycleRequest.from_json(json)
# print the JSON string representation of the object
print UpdateCycleRequest.to_json()

# convert the object into a dict
update_cycle_request_dict = update_cycle_request_instance.to_dict()
# create an instance of UpdateCycleRequest from a dict
update_cycle_request_from_dict = UpdateCycleRequest.from_dict(update_cycle_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


