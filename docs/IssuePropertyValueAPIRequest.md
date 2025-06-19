# IssuePropertyValueAPIRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value_text** | **str** |  | [optional] 
**value_boolean** | **bool** |  | [optional] 
**value_decimal** | **float** |  | [optional] 
**value_datetime** | **datetime** |  | [optional] 
**value_uuid** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**issue** | **str** |  | 
**var_property** | **str** |  | 
**value_option** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_property_value_api_request import IssuePropertyValueAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyValueAPIRequest from a JSON string
issue_property_value_api_request_instance = IssuePropertyValueAPIRequest.from_json(json)
# print the JSON string representation of the object
print IssuePropertyValueAPIRequest.to_json()

# convert the object into a dict
issue_property_value_api_request_dict = issue_property_value_api_request_instance.to_dict()
# create an instance of IssuePropertyValueAPIRequest from a dict
issue_property_value_api_request_from_dict = IssuePropertyValueAPIRequest.from_dict(issue_property_value_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


