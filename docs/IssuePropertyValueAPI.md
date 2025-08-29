# IssuePropertyValueAPI


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**value_text** | **str** |  | [optional] 
**value_boolean** | **bool** |  | [optional] 
**value_decimal** | **float** |  | [optional] 
**value_datetime** | **datetime** |  | [optional] 
**value_uuid** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**project** | **str** |  | [optional] [readonly] 
**issue** | **str** |  | 
**var_property** | **str** |  | 
**value_option** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_property_value_api import IssuePropertyValueAPI

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyValueAPI from a JSON string
issue_property_value_api_instance = IssuePropertyValueAPI.from_json(json)
# print the JSON string representation of the object
print(IssuePropertyValueAPI.to_json())

# convert the object into a dict
issue_property_value_api_dict = issue_property_value_api_instance.to_dict()
# create an instance of IssuePropertyValueAPI from a dict
issue_property_value_api_from_dict = IssuePropertyValueAPI.from_dict(issue_property_value_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


