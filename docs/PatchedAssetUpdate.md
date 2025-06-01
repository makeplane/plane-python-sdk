# PatchedAssetUpdate

Serializer for asset update requests after upload

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | **object** | Additional attributes to update for the asset | [optional] 

## Example

```python
from plane.models.patched_asset_update import PatchedAssetUpdate

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedAssetUpdate from a JSON string
patched_asset_update_instance = PatchedAssetUpdate.from_json(json)
# print the JSON string representation of the object
print PatchedAssetUpdate.to_json()

# convert the object into a dict
patched_asset_update_dict = patched_asset_update_instance.to_dict()
# create an instance of PatchedAssetUpdate from a dict
patched_asset_update_from_dict = PatchedAssetUpdate.from_dict(patched_asset_update_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


