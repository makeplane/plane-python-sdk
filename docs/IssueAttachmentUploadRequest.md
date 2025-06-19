# IssueAttachmentUploadRequest

Serializer for work item attachment upload request validation.  Handles file upload metadata validation including size, type, and external integration tracking for secure work item document attachment workflows.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Original filename of the asset | 
**type** | **str** | MIME type of the file | [optional] 
**size** | **int** | File size in bytes | 
**external_id** | **str** | External identifier for the asset (for integration tracking) | [optional] 
**external_source** | **str** | External source system (for integration tracking) | [optional] 

## Example

```python
from plane.models.issue_attachment_upload_request import IssueAttachmentUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueAttachmentUploadRequest from a JSON string
issue_attachment_upload_request_instance = IssueAttachmentUploadRequest.from_json(json)
# print the JSON string representation of the object
print IssueAttachmentUploadRequest.to_json()

# convert the object into a dict
issue_attachment_upload_request_dict = issue_attachment_upload_request_instance.to_dict()
# create an instance of IssueAttachmentUploadRequest from a dict
issue_attachment_upload_request_from_dict = IssueAttachmentUploadRequest.from_dict(issue_attachment_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


