# IntakeIssueCreateRequest

Serializer for creating intake work items with embedded issue data.  Manages intake work item creation including nested issue creation, status assignment, and source tracking for issue queue management.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issue** | [**IssueForIntakeRequest**](IssueForIntakeRequest.md) | Issue data for the intake issue | 
**intake** | **str** |  | 
**status** | [**IntakeIssueStatusEnum**](IntakeIssueStatusEnum.md) |  | [optional] 
**snoozed_till** | **datetime** |  | [optional] 
**duplicate_to** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**source_email** | **str** |  | [optional] 

## Example

```python
from plane.models.intake_issue_create_request import IntakeIssueCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IntakeIssueCreateRequest from a JSON string
intake_issue_create_request_instance = IntakeIssueCreateRequest.from_json(json)
# print the JSON string representation of the object
print IntakeIssueCreateRequest.to_json()

# convert the object into a dict
intake_issue_create_request_dict = intake_issue_create_request_instance.to_dict()
# create an instance of IntakeIssueCreateRequest from a dict
intake_issue_create_request_from_dict = IntakeIssueCreateRequest.from_dict(intake_issue_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


