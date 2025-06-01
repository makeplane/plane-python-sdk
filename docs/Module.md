# Module


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**members** | **List[str]** |  | [optional] 
**total_issues** | **int** |  | [readonly] 
**cancelled_issues** | **int** |  | [readonly] 
**completed_issues** | **int** |  | [readonly] 
**started_issues** | **int** |  | [readonly] 
**unstarted_issues** | **int** |  | [readonly] 
**backlog_issues** | **int** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**description_text** | **object** |  | [optional] 
**description_html** | **object** |  | [optional] 
**start_date** | **date** |  | [optional] 
**target_date** | **date** |  | [optional] 
**status** | **str** | * &#x60;backlog&#x60; - Backlog * &#x60;planned&#x60; - Planned * &#x60;in-progress&#x60; - In Progress * &#x60;paused&#x60; - Paused * &#x60;completed&#x60; - Completed * &#x60;cancelled&#x60; - Cancelled | [optional] 
**view_props** | **object** |  | [optional] 
**sort_order** | **float** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**archived_at** | **datetime** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**created_by** | **str** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 
**lead** | **str** |  | [optional] 

## Example

```python
from plane.models.module import Module

# TODO update the JSON string below
json = "{}"
# create an instance of Module from a JSON string
module_instance = Module.from_json(json)
# print the JSON string representation of the object
print Module.to_json()

# convert the object into a dict
module_dict = module_instance.to_dict()
# create an instance of Module from a dict
module_from_dict = Module.from_dict(module_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


