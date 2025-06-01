# StateLite


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**name** | **str** |  | [readonly] 
**color** | **str** |  | [readonly] 
**group** | **str** | * &#x60;backlog&#x60; - Backlog * &#x60;unstarted&#x60; - Unstarted * &#x60;started&#x60; - Started * &#x60;completed&#x60; - Completed * &#x60;cancelled&#x60; - Cancelled * &#x60;triage&#x60; - Triage | [readonly] 

## Example

```python
from plane.models.state_lite import StateLite

# TODO update the JSON string below
json = "{}"
# create an instance of StateLite from a JSON string
state_lite_instance = StateLite.from_json(json)
# print the JSON string representation of the object
print StateLite.to_json()

# convert the object into a dict
state_lite_dict = state_lite_instance.to_dict()
# create an instance of StateLite from a dict
state_lite_from_dict = StateLite.from_dict(state_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


