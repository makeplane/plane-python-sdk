# Project

Comprehensive project serializer with metrics and member context.  Provides complete project data including member counts, cycle/module totals, deployment status, and user-specific context for project management.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**total_members** | **int** |  | [optional] [readonly] 
**total_cycles** | **int** |  | [optional] [readonly] 
**total_modules** | **int** |  | [optional] [readonly] 
**is_member** | **bool** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] [readonly] 
**member_role** | **int** |  | [optional] [readonly] 
**is_deployed** | **bool** |  | [optional] [readonly] 
**cover_image_url** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**description_text** | **object** |  | [optional] 
**description_html** | **object** |  | [optional] 
**network** | [**NetworkEnum**](NetworkEnum.md) |  | [optional] 
**identifier** | **str** |  | 
**emoji** | **str** |  | [optional] [readonly] 
**icon_prop** | **object** |  | [optional] 
**module_view** | **bool** |  | [optional] 
**cycle_view** | **bool** |  | [optional] 
**issue_views_view** | **bool** |  | [optional] 
**page_view** | **bool** |  | [optional] 
**intake_view** | **bool** |  | [optional] 
**is_time_tracking_enabled** | **bool** |  | [optional] 
**is_issue_type_enabled** | **bool** |  | [optional] 
**guest_view_all_features** | **bool** |  | [optional] 
**cover_image** | **str** |  | [optional] 
**archive_in** | **int** |  | [optional] 
**close_in** | **int** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**default_assignee** | **str** |  | [optional] 
**project_lead** | **str** |  | [optional] 
**cover_image_asset** | **str** |  | [optional] 
**estimate** | **str** |  | [optional] 
**default_state** | **str** |  | [optional] 

## Example

```python
from plane.models.project import Project

# TODO update the JSON string below
json = "{}"
# create an instance of Project from a JSON string
project_instance = Project.from_json(json)
# print the JSON string representation of the object
print Project.to_json()

# convert the object into a dict
project_dict = project_instance.to_dict()
# create an instance of Project from a dict
project_from_dict = Project.from_dict(project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


