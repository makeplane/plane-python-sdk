# PageCreateAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**access** | [**PageCreateAPIAccessEnum**](PageCreateAPIAccessEnum.md) |  | [optional] 
**color** | **str** |  | [optional] 
**is_locked** | **bool** |  | [optional] 
**archived_at** | **date** |  | [optional] 
**view_props** | **object** |  | [optional] 
**logo_props** | **object** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**description_html** | **str** |  | 

## Example

```python
from plane.models.page_create_api_request import PageCreateAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PageCreateAPIRequest from a JSON string
page_create_api_request_instance = PageCreateAPIRequest.from_json(json)
# print the JSON string representation of the object
print(PageCreateAPIRequest.to_json())

# convert the object into a dict
page_create_api_request_dict = page_create_api_request_instance.to_dict()
# create an instance of PageCreateAPIRequest from a dict
page_create_api_request_from_dict = PageCreateAPIRequest.from_dict(page_create_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


