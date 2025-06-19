# PatchedIssuePropertyOptionAPIRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_property_option_api_request import PatchedIssuePropertyOptionAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssuePropertyOptionAPIRequest from a JSON string
patched_issue_property_option_api_request_instance = PatchedIssuePropertyOptionAPIRequest.from_json(json)
# print the JSON string representation of the object
print PatchedIssuePropertyOptionAPIRequest.to_json()

# convert the object into a dict
patched_issue_property_option_api_request_dict = patched_issue_property_option_api_request_instance.to_dict()
# create an instance of PatchedIssuePropertyOptionAPIRequest from a dict
patched_issue_property_option_api_request_from_dict = PatchedIssuePropertyOptionAPIRequest.from_dict(patched_issue_property_option_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


