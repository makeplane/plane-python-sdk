# CreateIntakeIssueRequestIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issue** | [**CreateIntakeIssueRequestIssueIssue**](CreateIntakeIssueRequestIssueIssue.md) |  | [optional] 

## Example

```python
from plane.models.create_intake_issue_request_issue import CreateIntakeIssueRequestIssue

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIntakeIssueRequestIssue from a JSON string
create_intake_issue_request_issue_instance = CreateIntakeIssueRequestIssue.from_json(json)
# print the JSON string representation of the object
print CreateIntakeIssueRequestIssue.to_json()

# convert the object into a dict
create_intake_issue_request_issue_dict = create_intake_issue_request_issue_instance.to_dict()
# create an instance of CreateIntakeIssueRequestIssue from a dict
create_intake_issue_request_issue_from_dict = CreateIntakeIssueRequestIssue.from_dict(create_intake_issue_request_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


