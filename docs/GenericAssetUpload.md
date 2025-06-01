# GenericAssetUpload

Serializer for generic asset upload requests

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Original filename of the asset | 
**type** | **str** | MIME type of the file | [optional] 
**size** | **int** | File size in bytes | 
**project_id** | **str** | UUID of the project to associate with the asset | [optional] 
**external_id** | **str** | External identifier for the asset (for integration tracking) | [optional] 
**external_source** | **str** | External source system (for integration tracking) | [optional] 

## Example

```python
from plane.models.generic_asset_upload import GenericAssetUpload

# TODO update the JSON string below
json = "{}"
# create an instance of GenericAssetUpload from a JSON string
generic_asset_upload_instance = GenericAssetUpload.from_json(json)
# print the JSON string representation of the object
print GenericAssetUpload.to_json()

# convert the object into a dict
generic_asset_upload_dict = generic_asset_upload_instance.to_dict()
# create an instance of GenericAssetUpload from a dict
generic_asset_upload_from_dict = GenericAssetUpload.from_dict(generic_asset_upload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


