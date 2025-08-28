# GenericAssetUploadRequest

Serializer for generic asset upload requests with project association.  Validates metadata for generating presigned URLs for workspace assets including project association, external system tracking, and file validation for document management and content storage workflows.

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
from plane.models.generic_asset_upload_request import GenericAssetUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of GenericAssetUploadRequest from a JSON string
generic_asset_upload_request_instance = GenericAssetUploadRequest.from_json(json)
# print the JSON string representation of the object
print(GenericAssetUploadRequest.to_json())

# convert the object into a dict
generic_asset_upload_request_dict = generic_asset_upload_request_instance.to_dict()
# create an instance of GenericAssetUploadRequest from a dict
generic_asset_upload_request_from_dict = GenericAssetUploadRequest.from_dict(generic_asset_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


