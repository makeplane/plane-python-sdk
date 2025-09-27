# IssueCommentCreateRequest

Serializer for creating work item comments.  Handles comment creation with JSON and HTML content support, access control, and external integration tracking.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comment_json** | **object** |  | [optional] 
**comment_html** | **str** |  | [optional] 
**access** | [**AccessBd4Enum**](AccessBd4Enum.md) |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_comment_create_request import IssueCommentCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueCommentCreateRequest from a JSON string
issue_comment_create_request_instance = IssueCommentCreateRequest.from_json(json)
# print the JSON string representation of the object
print(IssueCommentCreateRequest.to_json())

# convert the object into a dict
issue_comment_create_request_dict = issue_comment_create_request_instance.to_dict()
# create an instance of IssueCommentCreateRequest from a dict
issue_comment_create_request_from_dict = IssueCommentCreateRequest.from_dict(issue_comment_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


