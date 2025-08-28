# LabelCreateUpdateRequest

Serializer for creating and updating work item labels.  Manages label metadata including colors, descriptions, hierarchy, and sorting for work item categorization and filtering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**color** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**sort_order** | **float** |  | [optional] 

## Example

```python
from plane.models.label_create_update_request import LabelCreateUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LabelCreateUpdateRequest from a JSON string
label_create_update_request_instance = LabelCreateUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(LabelCreateUpdateRequest.to_json())

# convert the object into a dict
label_create_update_request_dict = label_create_update_request_instance.to_dict()
# create an instance of LabelCreateUpdateRequest from a dict
label_create_update_request_from_dict = LabelCreateUpdateRequest.from_dict(label_create_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


