# PatchedGenericAssetUpdate

Serializer for generic asset update requests

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_uploaded** | **bool** | Whether the asset has been successfully uploaded | [optional] [default to True]

## Example

```python
from plane.models.patched_generic_asset_update import PatchedGenericAssetUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedGenericAssetUpdate from a JSON string
patched_generic_asset_update_instance = PatchedGenericAssetUpdate.from_json(json)
# print the JSON string representation of the object
print PatchedGenericAssetUpdate.to_json()

# convert the object into a dict
patched_generic_asset_update_dict = patched_generic_asset_update_instance.to_dict()
# create an instance of PatchedGenericAssetUpdate from a dict
patched_generic_asset_update_from_dict = PatchedGenericAssetUpdate.from_dict(patched_generic_asset_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


