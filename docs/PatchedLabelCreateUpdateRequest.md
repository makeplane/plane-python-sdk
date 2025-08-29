# PatchedLabelCreateUpdateRequest

Serializer for creating and updating work item labels.  Manages label metadata including colors, descriptions, hierarchy, and sorting for work item categorization and filtering.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**description** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**sort_order** | **float** |  | [optional] 

## Example

```python
from plane.models.patched_label_create_update_request import PatchedLabelCreateUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedLabelCreateUpdateRequest from a JSON string
patched_label_create_update_request_instance = PatchedLabelCreateUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedLabelCreateUpdateRequest.to_json())

# convert the object into a dict
patched_label_create_update_request_dict = patched_label_create_update_request_instance.to_dict()
# create an instance of PatchedLabelCreateUpdateRequest from a dict
patched_label_create_update_request_from_dict = PatchedLabelCreateUpdateRequest.from_dict(patched_label_create_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


