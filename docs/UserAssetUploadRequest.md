# UserAssetUploadRequest

Serializer for user asset upload requests.  This serializer validates the metadata required to generate a presigned URL for uploading user profile assets (avatar or cover image) directly to S3 storage. Supports JPEG, PNG, WebP, JPG, and GIF image formats with size validation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Original filename of the asset | 
**type** | [**TypeEnum**](TypeEnum.md) | MIME type of the file  * &#x60;image/jpeg&#x60; - JPEG * &#x60;image/png&#x60; - PNG * &#x60;image/webp&#x60; - WebP * &#x60;image/jpg&#x60; - JPG * &#x60;image/gif&#x60; - GIF | [optional] 
**size** | **int** | File size in bytes | 
**entity_type** | [**EntityTypeEnum**](EntityTypeEnum.md) | Type of user asset  * &#x60;USER_AVATAR&#x60; - User Avatar * &#x60;USER_COVER&#x60; - User Cover | 

## Example

```python
from plane.models.user_asset_upload_request import UserAssetUploadRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UserAssetUploadRequest from a JSON string
user_asset_upload_request_instance = UserAssetUploadRequest.from_json(json)
# print the JSON string representation of the object
print(UserAssetUploadRequest.to_json())

# convert the object into a dict
user_asset_upload_request_dict = user_asset_upload_request_instance.to_dict()
# create an instance of UserAssetUploadRequest from a dict
user_asset_upload_request_from_dict = UserAssetUploadRequest.from_dict(user_asset_upload_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


