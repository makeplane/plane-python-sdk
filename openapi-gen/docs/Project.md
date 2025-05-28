# Project


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive_in** | **int** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**close_in** | **int** |  | [optional] 
**cover_image** | **str** |  | [optional] 
**cover_image_asset** | **str** |  | [optional] 
**cover_image_url** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**created_by** | **str** |  | [readonly] 
**cycle_view** | **bool** |  | [optional] 
**default_assignee** | **str** |  | [optional] 
**default_state** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [readonly] 
**description** | **str** |  | [optional] 
**description_html** | **object** |  | [optional] 
**description_text** | **object** |  | [optional] 
**emoji** | **str** |  | [readonly] 
**estimate** | **str** |  | [optional] 
**guest_view_all_features** | **bool** |  | [optional] 
**icon_prop** | **object** |  | [optional] 
**id** | **str** |  | [readonly] 
**identifier** | **str** |  | 
**inbox_view** | **bool** |  | [optional] 
**is_deployed** | **bool** |  | [readonly] 
**is_issue_type_enabled** | **bool** |  | [optional] 
**is_member** | **bool** |  | [readonly] 
**is_time_tracking_enabled** | **bool** |  | [optional] 
**issue_views_view** | **bool** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**member_role** | **int** |  | [readonly] 
**module_view** | **bool** |  | [optional] 
**name** | **str** |  | 
**network** | [**NetworkEnum**](NetworkEnum.md) |  | [optional] 
**page_view** | **bool** |  | [optional] 
**project_lead** | **str** |  | [optional] 
**sort_order** | **float** |  | [readonly] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**total_cycles** | **int** |  | [readonly] 
**total_members** | **int** |  | [readonly] 
**total_modules** | **int** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

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


