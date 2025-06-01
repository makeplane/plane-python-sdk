# AddCycleIssuesRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issues** | **List[str]** |  | [optional] 

## Example

```python
from plane.models.add_cycle_issues_request import AddCycleIssuesRequest

# TODO update the JSON string below
json = "{}"
# create an instance of AddCycleIssuesRequest from a JSON string
add_cycle_issues_request_instance = AddCycleIssuesRequest.from_json(json)
# print the JSON string representation of the object
print AddCycleIssuesRequest.to_json()

# convert the object into a dict
add_cycle_issues_request_dict = add_cycle_issues_request_instance.to_dict()
# create an instance of AddCycleIssuesRequest from a dict
add_cycle_issues_request_from_dict = AddCycleIssuesRequest.from_dict(add_cycle_issues_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


