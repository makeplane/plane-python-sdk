# PatchedIssueComment


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access** | [**AccessEnum**](AccessEnum.md) |  | [optional] 
**actor** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**comment_html** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_member** | **bool** |  | [optional] [readonly] 
**issue** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue_comment import PatchedIssueComment

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueComment from a JSON string
patched_issue_comment_instance = PatchedIssueComment.from_json(json)
# print the JSON string representation of the object
print PatchedIssueComment.to_json()

# convert the object into a dict
patched_issue_comment_dict = patched_issue_comment_instance.to_dict()
# create an instance of PatchedIssueComment from a dict
patched_issue_comment_from_dict = PatchedIssueComment.from_dict(patched_issue_comment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


