# IssueWorkLogAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**duration** | **int** |  | [optional] 
**created_by** | **str** |  | [optional] 
**updated_by** | **str** |  | [optional] 
**project_id** | **str** |  | [optional] [readonly] 
**workspace_id** | **str** |  | [optional] [readonly] 
**logged_by** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.issue_work_log_api import IssueWorkLogAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssueWorkLogAPI from a JSON string
issue_work_log_api_instance = IssueWorkLogAPI.from_json(json)
# print the JSON string representation of the object
print IssueWorkLogAPI.to_json()

# convert the object into a dict
issue_work_log_api_dict = issue_work_log_api_instance.to_dict()
# create an instance of IssueWorkLogAPI from a dict
issue_work_log_api_from_dict = IssueWorkLogAPI.from_dict(issue_work_log_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


