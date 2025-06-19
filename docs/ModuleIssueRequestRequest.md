# ModuleIssueRequestRequest

Serializer for bulk work item assignment to modules.  Validates work item ID lists for batch operations including module assignment and work item organization workflows.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | **List[str]** | List of issue IDs to add to the module | 

## Example

```python
from plane.models.module_issue_request_request import ModuleIssueRequestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ModuleIssueRequestRequest from a JSON string
module_issue_request_request_instance = ModuleIssueRequestRequest.from_json(json)
# print the JSON string representation of the object
print ModuleIssueRequestRequest.to_json()

# convert the object into a dict
module_issue_request_request_dict = module_issue_request_request_instance.to_dict()
# create an instance of ModuleIssueRequestRequest from a dict
module_issue_request_request_from_dict = ModuleIssueRequestRequest.from_dict(module_issue_request_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


