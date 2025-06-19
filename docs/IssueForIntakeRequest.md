# IssueForIntakeRequest

Serializer for work item data within intake submissions.  Handles essential work item fields for intake processing including content validation and priority assignment for triage workflows.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **object** |  | [optional] 
**description_html** | **str** |  | [optional] 
**priority** | [**PriorityEnum**](PriorityEnum.md) |  | [optional] 

## Example

```python
from plane.models.issue_for_intake_request import IssueForIntakeRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueForIntakeRequest from a JSON string
issue_for_intake_request_instance = IssueForIntakeRequest.from_json(json)
# print the JSON string representation of the object
print IssueForIntakeRequest.to_json()

# convert the object into a dict
issue_for_intake_request_dict = issue_for_intake_request_instance.to_dict()
# create an instance of IssueForIntakeRequest from a dict
issue_for_intake_request_from_dict = IssueForIntakeRequest.from_dict(issue_for_intake_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


