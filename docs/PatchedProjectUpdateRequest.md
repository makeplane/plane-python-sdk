# PatchedProjectUpdateRequest

Serializer for updating projects with enhanced state and estimation management.  Extends project creation with update-specific validations including default state assignment, estimation configuration, and project setting modifications.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**project_lead** | **str** |  | [optional] 
**default_assignee** | **str** |  | [optional] 
**identifier** | **str** |  | [optional] 
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
**default_state** | **str** |  | [optional] 
**estimate** | **str** |  | [optional] 

## Example

```python
from plane.models.patched_project_update_request import PatchedProjectUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedProjectUpdateRequest from a JSON string
patched_project_update_request_instance = PatchedProjectUpdateRequest.from_json(json)
# print the JSON string representation of the object
print PatchedProjectUpdateRequest.to_json()

# convert the object into a dict
patched_project_update_request_dict = patched_project_update_request_instance.to_dict()
# create an instance of PatchedProjectUpdateRequest from a dict
patched_project_update_request_from_dict = PatchedProjectUpdateRequest.from_dict(patched_project_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


