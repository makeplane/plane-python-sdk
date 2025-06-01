# CreateIntakeIssueRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issue** | [**CreateIntakeIssueRequestIssue**](CreateIntakeIssueRequestIssue.md) |  | [optional] 

## Example

```python
from plane.models.create_intake_issue_request import CreateIntakeIssueRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIntakeIssueRequest from a JSON string
create_intake_issue_request_instance = CreateIntakeIssueRequest.from_json(json)
# print the JSON string representation of the object
print CreateIntakeIssueRequest.to_json()

# convert the object into a dict
create_intake_issue_request_dict = create_intake_issue_request_instance.to_dict()
# create an instance of CreateIntakeIssueRequest from a dict
create_intake_issue_request_from_dict = CreateIntakeIssueRequest.from_dict(create_intake_issue_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


