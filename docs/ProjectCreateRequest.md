# ProjectCreateRequest

Serializer for creating projects with workspace validation.  Handles project creation including identifier validation, member verification, and workspace association for new project initialization.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**project_lead** | **str** |  | [optional] 
**default_assignee** | **str** |  | [optional] 
**identifier** | **str** |  | 
**icon_prop** | **object** |  | [optional] 
**emoji** | **str** |  | [optional] 
**cover_image** | **str** |  | [optional] 
**module_view** | **bool** |  | [optional] 
**cycle_view** | **bool** |  | [optional] 
**issue_views_view** | **bool** |  | [optional] 
**page_view** | **bool** |  | [optional] 
**intake_view** | **bool** |  | [optional] 
**guest_view_all_features** | **bool** |  | [optional] 
**archive_in** | **int** |  | [optional] 
**close_in** | **int** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**logo_props** | **object** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**is_issue_type_enabled** | **bool** |  | [optional] 

## Example

```python
from plane.models.project_create_request import ProjectCreateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ProjectCreateRequest from a JSON string
project_create_request_instance = ProjectCreateRequest.from_json(json)
# print the JSON string representation of the object
print(ProjectCreateRequest.to_json())

# convert the object into a dict
project_create_request_dict = project_create_request_instance.to_dict()
# create an instance of ProjectCreateRequest from a dict
project_create_request_from_dict = ProjectCreateRequest.from_dict(project_create_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


