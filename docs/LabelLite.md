# LabelLite

Lightweight label serializer for minimal data transfer.  Provides essential label information with visual properties, optimized for UI display and performance-critical operations.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**name** | **str** |  | 
**color** | **str** |  | [optional] 

## Example

```python
from plane.models.label_lite import LabelLite

# TODO update the JSON string below
json = "{}"
# create an instance of LabelLite from a JSON string
label_lite_instance = LabelLite.from_json(json)
# print the JSON string representation of the object
print LabelLite.to_json()

# convert the object into a dict
label_lite_dict = label_lite_instance.to_dict()
# create an instance of LabelLite from a dict
label_lite_from_dict = LabelLite.from_dict(label_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


