# PatchedGenericAssetUpdateRequest

Serializer for generic asset upload confirmation and status management.  Handles post-upload status updates for workspace assets including upload completion marking and metadata finalization.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_uploaded** | **bool** | Whether the asset has been successfully uploaded | [optional] [default to True]

## Example

```python
from plane.models.patched_generic_asset_update_request import PatchedGenericAssetUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedGenericAssetUpdateRequest from a JSON string
patched_generic_asset_update_request_instance = PatchedGenericAssetUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedGenericAssetUpdateRequest.to_json())

# convert the object into a dict
patched_generic_asset_update_request_dict = patched_generic_asset_update_request_instance.to_dict()
# create an instance of PatchedGenericAssetUpdateRequest from a dict
patched_generic_asset_update_request_from_dict = PatchedGenericAssetUpdateRequest.from_dict(patched_generic_asset_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


