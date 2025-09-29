# IssuePropertyAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relation_type** | [**IssuePropertyAPIRelationTypeEnum**](IssuePropertyAPIRelationTypeEnum.md) |  | [optional] 
**display_name** | **str** |  | 
**description** | **str** |  | [optional] 
**property_type** | [**PropertyTypeEnum**](PropertyTypeEnum.md) |  | 
**is_required** | **bool** |  | [optional] 
**default_value** | **List[str]** |  | [optional] 
**settings** | **object** |  | [optional] 
**is_active** | **bool** |  | [optional] 
**is_multi** | **bool** |  | [optional] 
**validation_rules** | **object** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 

## Example

```python
from plane.models.issue_property_api_request import IssuePropertyAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of IssuePropertyAPIRequest from a JSON string
issue_property_api_request_instance = IssuePropertyAPIRequest.from_json(json)
# print the JSON string representation of the object
print(IssuePropertyAPIRequest.to_json())

# convert the object into a dict
issue_property_api_request_dict = issue_property_api_request_instance.to_dict()
# create an instance of IssuePropertyAPIRequest from a dict
issue_property_api_request_from_dict = IssuePropertyAPIRequest.from_dict(issue_property_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


