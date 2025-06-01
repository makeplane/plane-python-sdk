# State


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [readonly] 
**created_at** | **datetime** |  | [readonly] 
**updated_at** | **datetime** |  | [readonly] 
**deleted_at** | **datetime** |  | [readonly] 
**name** | **str** |  | 
**description** | **str** |  | [optional] 
**color** | **str** |  | 
**slug** | **str** |  | [optional] 
**sequence** | **float** |  | [optional] 
**group** | **str** | * &#x60;backlog&#x60; - Backlog * &#x60;unstarted&#x60; - Unstarted * &#x60;started&#x60; - Started * &#x60;completed&#x60; - Completed * &#x60;cancelled&#x60; - Cancelled * &#x60;triage&#x60; - Triage | [optional] 
**is_triage** | **bool** |  | [optional] 
**default** | **bool** |  | [optional] 
**external_source** | **str** |  | [optional] 
**external_id** | **str** |  | [optional] 
**created_by** | **str** |  | [readonly] 
**updated_by** | **str** |  | [readonly] 
**project** | **str** |  | [readonly] 
**workspace** | **str** |  | [readonly] 

## Example

```python
from plane.models.state import State

# TODO update the JSON string below
json = "{}"
# create an instance of State from a JSON string
state_instance = State.from_json(json)
# print the JSON string representation of the object
print State.to_json()

# convert the object into a dict
state_dict = state_instance.to_dict()
# create an instance of State from a dict
state_from_dict = State.from_dict(state_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


