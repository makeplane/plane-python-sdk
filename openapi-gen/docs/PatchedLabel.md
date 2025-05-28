# PatchedLabel


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** |  | [optional] 
**created_at** | **datetime** |  | [optional] [readonly] 
**created_by** | **str** |  | [optional] [readonly] 
**deleted_at** | **datetime** |  | [optional] [readonly] 
**description** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**external_source** | **str** |  | [optional] 
**id** | **str** |  | [optional] [readonly] 
**name** | **str** |  | [optional] 
**parent** | **str** |  | [optional] 
**project** | **str** |  | [optional] [readonly] 
**sort_order** | **float** |  | [optional] 
**updated_at** | **datetime** |  | [optional] [readonly] 
**updated_by** | **str** |  | [optional] [readonly] 
**workspace** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.patched_label import PatchedLabel

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedLabel from a JSON string
patched_label_instance = PatchedLabel.from_json(json)
# print the JSON string representation of the object
print PatchedLabel.to_json()

# convert the object into a dict
patched_label_dict = patched_label_instance.to_dict()
# create an instance of PatchedLabel from a dict
patched_label_from_dict = PatchedLabel.from_dict(patched_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


