# PatchedInboxIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**duplicate_to** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**inbox** | **str** |  | [optional] 
**issue** | **str** |  | [optional] [readonly] 
**issue_detail** | [**IssueExpand**](IssueExpand.md) |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**snoozed_till** | **datetime** |  | [optional] 
**source** | **str** |  | [optional] 
**status** | [**InboxIssueStatusEnum**](InboxIssueStatusEnum.md) |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_inbox_issue import PatchedInboxIssue

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedInboxIssue from a JSON string
patched_inbox_issue_instance = PatchedInboxIssue.from_json(json)
# print the JSON string representation of the object
print PatchedInboxIssue.to_json()

# convert the object into a dict
patched_inbox_issue_dict = patched_inbox_issue_instance.to_dict()
# create an instance of PatchedInboxIssue from a dict
patched_inbox_issue_from_dict = PatchedInboxIssue.from_dict(patched_inbox_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


