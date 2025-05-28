# InboxIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**duplicate_to** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**inbox** | **str** |  | 
**issue** | **str** |  | [readonly] 
**issue_detail** | [**IssueExpand**](IssueExpand.md) |  | [readonly] 
**project** | **str** |  | [readonly] 
**snoozed_till** | **datetime** |  | [optional] 
**source** | **str** |  | [optional] 
**status** | [**InboxIssueStatusEnum**](InboxIssueStatusEnum.md) |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.inbox_issue import InboxIssue

# TODO update the JSON string below
json = "{}"
# create an instance of InboxIssue from a JSON string
inbox_issue_instance = InboxIssue.from_json(json)
# print the JSON string representation of the object
print InboxIssue.to_json()

# convert the object into a dict
inbox_issue_dict = inbox_issue_instance.to_dict()
# create an instance of InboxIssue from a dict
inbox_issue_from_dict = InboxIssue.from_dict(inbox_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


