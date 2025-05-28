# IssuePropertyOptionAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**logo_props** | **object** |  | [readonly] 
**name** | **str** |  | 
**parent** | **str** |  | [optional] 
**project** | **str** |  | [readonly] 
**var_property** | **str** |  | [readonly] 
**sort_order** | **float** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_property_option_api import IssuePropertyOptionAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyOptionAPI from a JSON string
issue_property_option_api_instance = IssuePropertyOptionAPI.from_json(json)
# print the JSON string representation of the object
print IssuePropertyOptionAPI.to_json()

# convert the object into a dict
issue_property_option_api_dict = issue_property_option_api_instance.to_dict()
# create an instance of IssuePropertyOptionAPI from a dict
issue_property_option_api_from_dict = IssuePropertyOptionAPI.from_dict(issue_property_option_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


