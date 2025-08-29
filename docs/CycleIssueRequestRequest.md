# CycleIssueRequestRequest

Serializer for bulk work item assignment to cycles.  Validates work item ID lists for batch operations including cycle assignment and sprint planning workflows.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | **List[str]** | List of issue IDs to add to the cycle | 

## Example

```python
from plane.models.cycle_issue_request_request import CycleIssueRequestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CycleIssueRequestRequest from a JSON string
cycle_issue_request_request_instance = CycleIssueRequestRequest.from_json(json)
# print the JSON string representation of the object
print(CycleIssueRequestRequest.to_json())

# convert the object into a dict
cycle_issue_request_request_dict = cycle_issue_request_request_instance.to_dict()
# create an instance of CycleIssueRequestRequest from a dict
cycle_issue_request_request_from_dict = CycleIssueRequestRequest.from_dict(cycle_issue_request_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


