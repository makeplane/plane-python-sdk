# IntakeIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**issue_detail** | [**IssueExpand**](IssueExpand.md) |  | [readonly] 
**inbox** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**status** | **int** | * &#x60;-2&#x60; - Pending * &#x60;-1&#x60; - Rejected * &#x60;0&#x60; - Snoozed * &#x60;1&#x60; - Accepted * &#x60;2&#x60; - Duplicate | [optional] 
**snoozed_till** | **datetime** |  | [optional] 
**source** | **str** |  | [optional] 
**source_email** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**extra** | **object** |  | [optional] 
**created_by** | **str** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 
**intake** | **str** |  | 
**issue** | **str** |  | [readonly] 
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


