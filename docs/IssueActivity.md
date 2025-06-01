# IssueActivity


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [optional] 
**verb** | **str** |  | [optional] 
**field** | **str** |  | [optional] 
**old_value** | **str** |  | [optional] 
**new_value** | **str** |  | [optional] 
**comment** | **str** |  | [optional] 
**attachments** | **List[str]** |  | [optional] 
**old_identifier** | **str** |  | [optional] 
**new_identifier** | **str** |  | [optional] 
**epoch** | **float** |  | [optional] 
**project** | **str** |  | 
**workspace** | **str** |  | 
**issue** | **str** |  | [optional] 
**issue_comment** | **str** |  | [optional] 
**actor** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_activity import IssueActivity

# TODO update the JSON string below
json = "{}"
# create an instance of IssueActivity from a JSON string
issue_activity_instance = IssueActivity.from_json(json)
# print the JSON string representation of the object
print IssueActivity.to_json()

# convert the object into a dict
issue_activity_dict = issue_activity_instance.to_dict()
# create an instance of IssueActivity from a dict
issue_activity_from_dict = IssueActivity.from_dict(issue_activity_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


