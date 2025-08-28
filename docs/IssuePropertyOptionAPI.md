# IssuePropertyOptionAPI


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | 
**sort_order** | **float** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**logo_props** | **object** |  | [optional] [readonly] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**var_property** | **str** |  | [optional] [readonly] 
**parent** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_property_option_api import IssuePropertyOptionAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyOptionAPI from a JSON string
issue_property_option_api_instance = IssuePropertyOptionAPI.from_json(json)
# print the JSON string representation of the object
print(IssuePropertyOptionAPI.to_json())

# convert the object into a dict
issue_property_option_api_dict = issue_property_option_api_instance.to_dict()
# create an instance of IssuePropertyOptionAPI from a dict
issue_property_option_api_from_dict = IssuePropertyOptionAPI.from_dict(issue_property_option_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


