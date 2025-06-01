# UpdateLabelRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**color** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from plane.models.update_label_request import UpdateLabelRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateLabelRequest from a JSON string
update_label_request_instance = UpdateLabelRequest.from_json(json)
# print the JSON string representation of the object
print UpdateLabelRequest.to_json()

# convert the object into a dict
update_label_request_dict = update_label_request_instance.to_dict()
# create an instance of UpdateLabelRequest from a dict
update_label_request_from_dict = UpdateLabelRequest.from_dict(update_label_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


