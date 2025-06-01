# CreateIssueCommentRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comment_html** | **str** |  | 

## Example

```python
from plane.models.create_issue_comment_request import CreateIssueCommentRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIssueCommentRequest from a JSON string
create_issue_comment_request_instance = CreateIssueCommentRequest.from_json(json)
# print the JSON string representation of the object
print CreateIssueCommentRequest.to_json()

# convert the object into a dict
create_issue_comment_request_dict = create_issue_comment_request_instance.to_dict()
# create an instance of CreateIssueCommentRequest from a dict
create_issue_comment_request_from_dict = CreateIssueCommentRequest.from_dict(create_issue_comment_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


