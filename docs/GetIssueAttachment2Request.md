# GetIssueAttachment2Request


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Original filename of the asset | [optional] 
**type** | **str** | MIME type of the file | [optional] 
**size** | **int** | File size in bytes | [optional] 
**external_id** | **str** | External identifier for the asset (for integration tracking) | [optional] 
**external_source** | **str** | External source system (for integration tracking) | [optional] 

## Example

```python
from plane.models.get_issue_attachment2_request import GetIssueAttachment2Request

# TODO update the JSON string below
json = "{}"
# create an instance of GetIssueAttachment2Request from a JSON string
get_issue_attachment2_request_instance = GetIssueAttachment2Request.from_json(json)
# print the JSON string representation of the object
print GetIssueAttachment2Request.to_json()

# convert the object into a dict
get_issue_attachment2_request_dict = get_issue_attachment2_request_instance.to_dict()
# create an instance of GetIssueAttachment2Request from a dict
get_issue_attachment2_request_from_dict = GetIssueAttachment2Request.from_dict(get_issue_attachment2_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


