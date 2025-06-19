# IntakeIssue

Comprehensive serializer for intake work items with expanded issue details.  Provides full intake work item data including embedded issue information, status tracking, and triage metadata for issue queue management.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**issue_detail** | [**IssueExpand**](IssueExpand.md) |  | [optional] [readonly] 
**inbox** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**status** | [**IntakeIssueStatusEnum**](IntakeIssueStatusEnum.md) |  | [optional] 
**snoozed_till** | **datetime** |  | [optional] 
**source** | **str** |  | [optional] 
**source_email** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**extra** | **object** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**intake** | **str** |  | 
**issue** | **str** |  | [optional] [readonly] 
**duplicate_to** | **str** |  | [optional] 

## Example

```python
from plane.models.intake_issue import IntakeIssue

# TODO update the JSON string below
json = "{}"
# create an instance of IntakeIssue from a JSON string
intake_issue_instance = IntakeIssue.from_json(json)
# print the JSON string representation of the object
print IntakeIssue.to_json()

# convert the object into a dict
intake_issue_dict = intake_issue_instance.to_dict()
# create an instance of IntakeIssue from a dict
intake_issue_from_dict = IntakeIssue.from_dict(intake_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


