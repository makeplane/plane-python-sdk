# CreateModuleRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Module name | [optional] 
**description** | **str** | Module description | [optional] 
**start_date** | **datetime** | Start date | [optional] 
**target_date** | **datetime** | Target date | [optional] 
**status** | **str** | Module status | [optional] 
**lead** | **str** | Lead user ID | [optional] 
**members** | **List[str]** |  | [optional] 

## Example

```python
from plane.models.create_module_request import CreateModuleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateModuleRequest from a JSON string
create_module_request_instance = CreateModuleRequest.from_json(json)
# print the JSON string representation of the object
print CreateModuleRequest.to_json()

# convert the object into a dict
create_module_request_dict = create_module_request_instance.to_dict()
# create an instance of CreateModuleRequest from a dict
create_module_request_from_dict = CreateModuleRequest.from_dict(create_module_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


