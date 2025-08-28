# PatchedIssueWorkLogAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**duration** | **int** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_work_log_api_request import PatchedIssueWorkLogAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueWorkLogAPIRequest from a JSON string
patched_issue_work_log_api_request_instance = PatchedIssueWorkLogAPIRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedIssueWorkLogAPIRequest.to_json())

# convert the object into a dict
patched_issue_work_log_api_request_dict = patched_issue_work_log_api_request_instance.to_dict()
# create an instance of PatchedIssueWorkLogAPIRequest from a dict
patched_issue_work_log_api_request_from_dict = PatchedIssueWorkLogAPIRequest.from_dict(patched_issue_work_log_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


