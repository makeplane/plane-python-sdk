# PatchedIssuePropertyOptionAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**is_active** | **bool** |  | [optional] 
**is_default** | **bool** |  | [optional] 
**logo_props** | **object** |  | [optional] [readonly] 
**name** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**var_property** | **str** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_issue_property_option_api import PatchedIssuePropertyOptionAPI

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedIssuePropertyOptionAPI from a JSON string
patched_issue_property_option_api_instance = PatchedIssuePropertyOptionAPI.from_json(json)
# print the JSON string representation of the object
print PatchedIssuePropertyOptionAPI.to_json()

# convert the object into a dict
patched_issue_property_option_api_dict = patched_issue_property_option_api_instance.to_dict()
# create an instance of PatchedIssuePropertyOptionAPI from a dict
patched_issue_property_option_api_from_dict = PatchedIssuePropertyOptionAPI.from_dict(patched_issue_property_option_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


