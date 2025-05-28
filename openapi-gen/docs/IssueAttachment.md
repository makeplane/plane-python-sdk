# IssueAttachment


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**asset** | **str** |  | 
**attributes** | **object** |  | [optional] 
**comment** | **str** |  | [optional] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] 
**draft_issue** | **str** |  | [optional] 
**entity_type** | [**IssueAttachmentEntityType**](IssueAttachmentEntityType.md) |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_archived** | **bool** |  | [optional] 
**is_deleted** | **bool** |  | [optional] 
**is_uploaded** | **bool** |  | [optional] 
**issue** | **str** |  | [readonly] 
**page** | **str** |  | [optional] 
**project** | **str** |  | [readonly] 
**size** | **float** |  | [optional] 
**storage_metadata** | **object** |  | [optional] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**user** | **str** |  | [optional] 
**workspace** | **str** |  | [readonly] 

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


