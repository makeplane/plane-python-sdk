# LabelLite


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**color** | **str** |  | [optional] 
**id** | **str** |  | [readonly] 
**name** | **str** |  | 

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


