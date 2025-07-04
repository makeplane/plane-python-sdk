# UserLite

Lightweight user serializer for minimal data transfer.  Provides essential user information including names, avatar, and contact details optimized for member lists, assignee displays, and user references.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | [optional] [readonly] 
**first_name** | **str** |  | [optional] [readonly] 
**last_name** | **str** |  | [optional] [readonly] 
**email** | **str** |  | [optional] [readonly] 
**avatar** | **str** |  | [optional] [readonly] 
**avatar_url** | **str** | Avatar URL | [optional] [readonly] 
**display_name** | **str** |  | [optional] [readonly] 

## Example

```python
from plane.models.user_lite import UserLite

# TODO update the JSON string below
json = "{}"
# create an instance of UserLite from a JSON string
user_lite_instance = UserLite.from_json(json)
# print the JSON string representation of the object
print UserLite.to_json()

# convert the object into a dict
user_lite_dict = user_lite_instance.to_dict()
# create an instance of UserLite from a dict
user_lite_from_dict = UserLite.from_dict(user_lite_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


