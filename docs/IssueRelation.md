# IssueRelation

Serializer for issue relationships showing related issue details.  Provides comprehensive information about related issues including project context, sequence ID, and relationship type.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**project_id** | **str** |  | [optional] [readonly] 
**sequence_id** | **int** |  | [optional] [readonly] 
**relation_type** | **str** |  | [optional] [readonly] 
**name** | **str** |  | [optional] [readonly] 
**type_id** | **str** |  | [optional] [readonly] 
**is_epic** | **bool** |  | [optional] [readonly] 
**state_id** | **str** |  | [optional] [readonly] 
**priority** | **str** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.issue_relation import IssueRelation

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRelation from a JSON string
issue_relation_instance = IssueRelation.from_json(json)
# print the JSON string representation of the object
print(IssueRelation.to_json())

# convert the object into a dict
issue_relation_dict = issue_relation_instance.to_dict()
# create an instance of IssueRelation from a dict
issue_relation_from_dict = IssueRelation.from_dict(issue_relation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


