# ModuleIssue


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | 
**id** | **str** |  | [readonly] 
**issue** | **str** |  | 
**module** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**sub_issues_count** | **int** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.module_issue import ModuleIssue

# TODO update the JSON string below
json = "{}"
# create an instance of ModuleIssue from a JSON string
module_issue_instance = ModuleIssue.from_json(json)
# print the JSON string representation of the object
print ModuleIssue.to_json()

# convert the object into a dict
module_issue_dict = module_issue_instance.to_dict()
# create an instance of ModuleIssue from a dict
module_issue_from_dict = ModuleIssue.from_dict(module_issue_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


