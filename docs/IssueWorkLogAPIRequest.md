# IssueWorkLogAPIRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** |  | [optional] 
**duration** | **int** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_work_log_api_request import IssueWorkLogAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueWorkLogAPIRequest from a JSON string
issue_work_log_api_request_instance = IssueWorkLogAPIRequest.from_json(json)
# print the JSON string representation of the object
print IssueWorkLogAPIRequest.to_json()

# convert the object into a dict
issue_work_log_api_request_dict = issue_work_log_api_request_instance.to_dict()
# create an instance of IssueWorkLogAPIRequest from a dict
issue_work_log_api_request_from_dict = IssueWorkLogAPIRequest.from_dict(issue_work_log_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


