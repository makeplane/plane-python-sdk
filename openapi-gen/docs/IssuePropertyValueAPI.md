# IssuePropertyValueAPI


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**issue** | **str** |  | 
**project** | **str** |  | [readonly] 
**var_property** | **str** |  | 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**value_boolean** | **bool** |  | [optional] 
**value_datetime** | **datetime** |  | [optional] 
**value_decimal** | **float** |  | [optional] 
**value_option** | **str** |  | [optional] 
**value_text** | **str** |  | [optional] 
**value_uuid** | **str** |  | [optional] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.issue_property_value_api import IssuePropertyValueAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyValueAPI from a JSON string
issue_property_value_api_instance = IssuePropertyValueAPI.from_json(json)
# print the JSON string representation of the object
print IssuePropertyValueAPI.to_json()

# convert the object into a dict
issue_property_value_api_dict = issue_property_value_api_instance.to_dict()
# create an instance of IssuePropertyValueAPI from a dict
issue_property_value_api_from_dict = IssuePropertyValueAPI.from_dict(issue_property_value_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


