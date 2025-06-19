# PatchedIssueTypeAPIRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_ids** | **List[str]** |  | [optional] 
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**is_epic** | **bool** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_type_api_request import PatchedIssueTypeAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueTypeAPIRequest from a JSON string
patched_issue_type_api_request_instance = PatchedIssueTypeAPIRequest.from_json(json)
# print the JSON string representation of the object
print PatchedIssueTypeAPIRequest.to_json()

# convert the object into a dict
patched_issue_type_api_request_dict = patched_issue_type_api_request_instance.to_dict()
# create an instance of PatchedIssueTypeAPIRequest from a dict
patched_issue_type_api_request_from_dict = PatchedIssueTypeAPIRequest.from_dict(patched_issue_type_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


