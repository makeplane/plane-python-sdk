# ProjectWorklogSummary

Serializer for project worklog summary with aggregated duration per issue

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**issue_id** | **str** | ID of the work item | 
**duration** | **int** | Total duration logged for this work item in seconds | 

## Example

```python
from plane.models.project_worklog_summary import ProjectWorklogSummary

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectWorklogSummary from a JSON string
project_worklog_summary_instance = ProjectWorklogSummary.from_json(json)
# print the JSON string representation of the object
print ProjectWorklogSummary.to_json()

# convert the object into a dict
project_worklog_summary_dict = project_worklog_summary_instance.to_dict()
# create an instance of ProjectWorklogSummary from a dict
project_worklog_summary_from_dict = ProjectWorklogSummary.from_dict(project_worklog_summary_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


