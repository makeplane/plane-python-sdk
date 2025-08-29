# IssueTypeAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**project_ids** | **List[str]** |  | [optional] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**is_epic** | **bool** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_type_api_request import IssueTypeAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssueTypeAPIRequest from a JSON string
issue_type_api_request_instance = IssueTypeAPIRequest.from_json(json)
# print the JSON string representation of the object
print(IssueTypeAPIRequest.to_json())

# convert the object into a dict
issue_type_api_request_dict = issue_type_api_request_instance.to_dict()
# create an instance of IssueTypeAPIRequest from a dict
issue_type_api_request_from_dict = IssueTypeAPIRequest.from_dict(issue_type_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


