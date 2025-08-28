# TransferCycleIssueRequestRequest

Serializer for transferring work items between cycles.  Handles work item migration between cycles including validation and relationship updates for sprint reallocation workflows.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**new_cycle_id** | **str** | ID of the target cycle to transfer issues to | 

## Example

```python
from plane.models.transfer_cycle_issue_request_request import TransferCycleIssueRequestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TransferCycleIssueRequestRequest from a JSON string
transfer_cycle_issue_request_request_instance = TransferCycleIssueRequestRequest.from_json(json)
# print the JSON string representation of the object
print(TransferCycleIssueRequestRequest.to_json())

# convert the object into a dict
transfer_cycle_issue_request_request_dict = transfer_cycle_issue_request_request_instance.to_dict()
# create an instance of TransferCycleIssueRequestRequest from a dict
transfer_cycle_issue_request_request_from_dict = TransferCycleIssueRequestRequest.from_dict(transfer_cycle_issue_request_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


