# IssuePropertyAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**default_value** | **List[str]** |  | [optional] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**display_name** | **str** |  | 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_active** | **bool** |  | [optional] 
**is_multi** | **bool** |  | [optional] 
**is_required** | **bool** |  | [optional] 
**issue_type** | **str** |  | [readonly] 
**logo_props** | **object** |  | [readonly] 
**name** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**property_type** | [**PropertyTypeEnum**](PropertyTypeEnum.md) |  | 
**relation_type** | [**IssuePropertyAPIRelationType**](IssuePropertyAPIRelationType.md) |  | [optional] 
**settings** | **object** |  | [readonly] 
**sort_order** | **float** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**validation_rules** | **object** |  | [optional] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_property_api import IssuePropertyAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyAPI from a JSON string
issue_property_api_instance = IssuePropertyAPI.from_json(json)
# print the JSON string representation of the object
print IssuePropertyAPI.to_json()

# convert the object into a dict
issue_property_api_dict = issue_property_api_instance.to_dict()
# create an instance of IssuePropertyAPI from a dict
issue_property_api_from_dict = IssuePropertyAPI.from_dict(issue_property_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


