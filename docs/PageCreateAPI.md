# PageCreateAPI


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**name** | **str** |  | 
**owned_by** | **str** |  | [optional] [readonly] 
**access** | [**PageCreateAPIAccessEnum**](PageCreateAPIAccessEnum.md) |  | [optional] 
**color** | **str** |  | [optional] 
**is_locked** | **bool** |  | [optional] 
**archived_at** | **date** |  | [optional] 
**workspace** | **str** |  | [optional] [readonly] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**view_props** | **object** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**parent_id** | **str** |  | [optional] [readonly] 
**description_html** | **str** |  | 

## Example

```python
from plane.models.page_create_api import PageCreateAPI

# TODO update the JSON string below
json = "{}"
# create an instance of PageCreateAPI from a JSON string
page_create_api_instance = PageCreateAPI.from_json(json)
# print the JSON string representation of the object
print(PageCreateAPI.to_json())

# convert the object into a dict
page_create_api_dict = page_create_api_instance.to_dict()
# create an instance of PageCreateAPI from a dict
page_create_api_from_dict = PageCreateAPI.from_dict(page_create_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


