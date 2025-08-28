# PatchedAssetUpdateRequest

Serializer for asset status updates after successful upload completion.  Handles post-upload asset metadata updates including attribute modifications and upload confirmation for S3-based file storage workflows.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | **object** | Additional attributes to update for the asset | [optional] 

## Example

```python
from plane.models.patched_asset_update_request import PatchedAssetUpdateRequest

# TODO update the JSON string below
json = "{}"
# create an instance of PatchedAssetUpdateRequest from a JSON string
patched_asset_update_request_instance = PatchedAssetUpdateRequest.from_json(json)
# print the JSON string representation of the object
print(PatchedAssetUpdateRequest.to_json())

# convert the object into a dict
patched_asset_update_request_dict = patched_asset_update_request_instance.to_dict()
# create an instance of PatchedAssetUpdateRequest from a dict
patched_asset_update_request_from_dict = PatchedAssetUpdateRequest.from_dict(patched_asset_update_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


