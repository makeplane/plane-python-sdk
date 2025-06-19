# IssueAttachment

Serializer for work item file attachments.  Manages file asset associations with work items including metadata, storage information, and access control for document management.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**attributes** | **object** |  | [optional] 
**asset** | **str** |  | 
**entity_type** | **str** |  | [optional] 
**entity_identifier** | **str** |  | [optional] 
**is_deleted** | **bool** |  | [optional] 
**is_archived** | **bool** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**size** | **float** |  | [optional] 
**is_uploaded** | **bool** |  | [optional] 
**storage_metadata** | **object** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] [readonly] 
**user** | **str** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 
**draft_issue** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | [optional] [readonly] 
**comment** | **str** |  | [optional] 
**page** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_attachment import IssueAttachment

# TODO update the JSON string below
json = "{}"
# create an instance of IssueAttachment from a JSON string
issue_attachment_instance = IssueAttachment.from_json(json)
# print the JSON string representation of the object
print IssueAttachment.to_json()

# convert the object into a dict
issue_attachment_dict = issue_attachment_instance.to_dict()
# create an instance of IssueAttachment from a dict
issue_attachment_from_dict = IssueAttachment.from_dict(issue_attachment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


