# PageDetailAPI


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**name** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**owned_by** | **str** |  | [optional] [readonly] 
**anchor** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 
**projects** | **List[str]** |  | [optional] [readonly] 

## Example

```python
from plane.models.page_detail_api import PageDetailAPI

# TODO update the JSON string below
json = "{}"
# create an instance of PageDetailAPI from a JSON string
page_detail_api_instance = PageDetailAPI.from_json(json)
# print the JSON string representation of the object
print(PageDetailAPI.to_json())

# convert the object into a dict
page_detail_api_dict = page_detail_api_instance.to_dict()
# create an instance of PageDetailAPI from a dict
page_detail_api_from_dict = PageDetailAPI.from_dict(page_detail_api_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


