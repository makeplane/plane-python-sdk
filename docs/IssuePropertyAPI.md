# IssuePropertyAPI


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**relation_type** | [**RelationTypeEnum**](RelationTypeEnum.md) |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | [optional] [readonly] 
**display_name** | **str** |  | 
**description** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] [readonly] 
**property_type** | [**PropertyTypeEnum**](PropertyTypeEnum.md) |  | 
**is_required** | **bool** |  | [optional] 
**default_value** | **List[str]** |  | [optional] 
**settings** | **object** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**is_multi** | **bool** |  | [optional] 
**validation_rules** | **object** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**issue_type** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.issue_property_api import IssuePropertyAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyAPI from a JSON string
issue_property_api_instance = IssuePropertyAPI.from_json(json)
# print the JSON string representation of the object
print(IssuePropertyAPI.to_json())

# convert the object into a dict
issue_property_api_dict = issue_property_api_instance.to_dict()
# create an instance of IssuePropertyAPI from a dict
issue_property_api_from_dict = IssuePropertyAPI.from_dict(issue_property_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


