# CreateIntakeIssueRequestIssueIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Issue name | [optional] 
**description_html** | **str** | Issue description HTML | [optional] 
**priority** | **str** | Issue priority | [optional] 

## Example

```python
from plane.models.create_intake_issue_request_issue_issue import CreateIntakeIssueRequestIssueIssue

# TODO update the JSON string below
json = "{}"
# create an instance of CreateIntakeIssueRequestIssueIssue from a JSON string
create_intake_issue_request_issue_issue_instance = CreateIntakeIssueRequestIssueIssue.from_json(json)
# print the JSON string representation of the object
print CreateIntakeIssueRequestIssueIssue.to_json()

# convert the object into a dict
create_intake_issue_request_issue_issue_dict = create_intake_issue_request_issue_issue_instance.to_dict()
# create an instance of CreateIntakeIssueRequestIssueIssue from a dict
create_intake_issue_request_issue_issue_from_dict = CreateIntakeIssueRequestIssueIssue.from_dict(create_intake_issue_request_issue_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


