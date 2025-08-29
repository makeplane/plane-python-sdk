# PatchedIssueCommentCreateRequest

Serializer for creating work item comments.  Handles comment creation with JSON and HTML content support, access control, and external integration tracking.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comment_json** | **object** |  | [optional] 
**comment_html** | **str** |  | [optional] 
**access** | [**AccessEnum**](AccessEnum.md) |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_issue_comment_create_request import PatchedIssueCommentCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssueCommentCreateRequest from a JSON string
patched_issue_comment_create_request_instance = PatchedIssueCommentCreateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedIssueCommentCreateRequest.to_json())

# convert the object into a dict
patched_issue_comment_create_request_dict = patched_issue_comment_create_request_instance.to_dict()
# create an instance of PatchedIssueCommentCreateRequest from a dict
patched_issue_comment_create_request_from_dict = PatchedIssueCommentCreateRequest.from_dict(patched_issue_comment_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


