# PatchedIntakeIssueUpdateRequest

Serializer for updating intake work items and their associated issues.  Handles intake work item modifications including status changes, triage decisions, and embedded issue updates for issue queue processing workflows.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**IntakeIssueStatusEnum**](IntakeIssueStatusEnum.md) |  | [optional] 
**snoozed_till** | **datetime** |  | [optional] 
**duplicate_to** | **str** |  | [optional] 
**source** | **str** |  | [optional] 
**source_email** | **str** |  | [optional] 
**issue** | [**IssueForIntakeRequest**](IssueForIntakeRequest.md) | Issue data to update in the intake issue | [optional] 

## Example

```python
from plane.models.patched_intake_issue_update_request import PatchedIntakeIssueUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIntakeIssueUpdateRequest from a JSON string
patched_intake_issue_update_request_instance = PatchedIntakeIssueUpdateRequest.from_json(json)
# print the JSON string representation of the object
print PatchedIntakeIssueUpdateRequest.to_json()

# convert the object into a dict
patched_intake_issue_update_request_dict = patched_intake_issue_update_request_instance.to_dict()
# create an instance of PatchedIntakeIssueUpdateRequest from a dict
patched_intake_issue_update_request_from_dict = PatchedIntakeIssueUpdateRequest.from_dict(patched_intake_issue_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


