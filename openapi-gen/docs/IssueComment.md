# IssueComment


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access** | [**AccessEnum**](AccessEnum.md) |  | [optional] 
**actor** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**comment_html** | **str** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_member** | **bool** |  | [readonly] 
**issue** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_comment import IssueComment

# TODO update the JSON string below
json = "{}"
# create an instance of IssueComment from a JSON string
issue_comment_instance = IssueComment.from_json(json)
# print the JSON string representation of the object
print IssueComment.to_json()

# convert the object into a dict
issue_comment_dict = issue_comment_instance.to_dict()
# create an instance of IssueComment from a dict
issue_comment_from_dict = IssueComment.from_dict(issue_comment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


