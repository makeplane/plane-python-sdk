# PageDetailAPIRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**description_stripped** | **str** |  | [optional] 

## Example

```python
from plane.models.page_detail_api_request import PageDetailAPIRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PageDetailAPIRequest from a JSON string
page_detail_api_request_instance = PageDetailAPIRequest.from_json(json)
# print the JSON string representation of the object
print(PageDetailAPIRequest.to_json())

# convert the object into a dict
page_detail_api_request_dict = page_detail_api_request_instance.to_dict()
# create an instance of PageDetailAPIRequest from a dict
page_detail_api_request_from_dict = PageDetailAPIRequest.from_dict(page_detail_api_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


