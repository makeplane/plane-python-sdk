# IssueComment

Full serializer for work item comments with membership context.  Provides complete comment data including member status, content formatting, and edit tracking for collaborative work item discussions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**is_member** | **bool** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**comment_stripped** | **str** |  | [optional] 
**comment_html** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**access** | [**AccessEnum**](AccessEnum.md) |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**edited_at** | **datetime** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | [optional] [readonly] 
**actor** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_comment import IssueComment

# TODO update the JSON string below
json = "{}"
# create an instance of IssueComment from a JSON string
issue_comment_instance = IssueComment.from_json(json)
# print the JSON string representation of the object
print(IssueComment.to_json())

# convert the object into a dict
issue_comment_dict = issue_comment_instance.to_dict()
# create an instance of IssueComment from a dict
issue_comment_from_dict = IssueComment.from_dict(issue_comment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


