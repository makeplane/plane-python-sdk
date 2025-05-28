# PatchedProject


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**archive_in** | **int** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**close_in** | **int** |  | [optional] 
**cover_image** | **str** |  | [optional] 
**cover_image_asset** | **str** |  | [optional] 
**cover_image_url** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**cycle_view** | **bool** |  | [optional] 
**default_assignee** | **str** |  | [optional] 
**default_state** | **str** |  | [optional] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**description_html** | **object** |  | [optional] 
**description_text** | **object** |  | [optional] 
**emoji** | **str** |  | [optional] [readonly] 
**estimate** | **str** |  | [optional] 
**guest_view_all_features** | **bool** |  | [optional] 
**icon_prop** | **object** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**identifier** | **str** |  | [optional] 
**inbox_view** | **bool** |  | [optional] 
**is_deployed** | **bool** |  | [optional] [readonly] 
**is_issue_type_enabled** | **bool** |  | [optional] 
**is_member** | **bool** |  | [optional] [readonly] 
**is_time_tracking_enabled** | **bool** |  | [optional] 
**issue_views_view** | **bool** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**member_role** | **int** |  | [optional] [readonly] 
**module_view** | **bool** |  | [optional] 
**name** | **str** |  | [optional] 
**network** | [**NetworkEnum**](NetworkEnum.md) |  | [optional] 
**page_view** | **bool** |  | [optional] 
**project_lead** | **str** |  | [optional] 
**sort_order** | **float** |  | [optional] [readonly] 
**timezone** | [**TimezoneEnum**](TimezoneEnum.md) |  | [optional] 
**total_cycles** | **int** |  | [optional] [readonly] 
**total_members** | **int** |  | [optional] [readonly] 
**total_modules** | **int** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_project import PatchedProject

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedProject from a JSON string
patched_project_instance = PatchedProject.from_json(json)
# print the JSON string representation of the object
print PatchedProject.to_json()

# convert the object into a dict
patched_project_dict = patched_project_instance.to_dict()
# create an instance of PatchedProject from a dict
patched_project_from_dict = PatchedProject.from_dict(patched_project_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


