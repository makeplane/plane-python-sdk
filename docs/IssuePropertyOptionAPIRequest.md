# IssuePropertyOptionAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_property_option_api_request import IssuePropertyOptionAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyOptionAPIRequest from a JSON string
issue_property_option_api_request_instance = IssuePropertyOptionAPIRequest.from_json(json)
# print the JSON string representation of the object
print(IssuePropertyOptionAPIRequest.to_json())

# convert the object into a dict
issue_property_option_api_request_dict = issue_property_option_api_request_instance.to_dict()
# create an instance of IssuePropertyOptionAPIRequest from a dict
issue_property_option_api_request_from_dict = IssuePropertyOptionAPIRequest.from_dict(issue_property_option_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


