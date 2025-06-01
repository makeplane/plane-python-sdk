# UserAssetUpload

Serializer for user asset upload requests

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Original filename of the asset | 
**type** | **str** | MIME type of the file  * &#x60;image/jpeg&#x60; - JPEG * &#x60;image/png&#x60; - PNG * &#x60;image/webp&#x60; - WebP * &#x60;image/jpg&#x60; - JPG * &#x60;image/gif&#x60; - GIF | [optional] [default to 'image/jpeg']
**size** | **int** | File size in bytes | 
**entity_type** | **str** | Type of user asset  * &#x60;USER_AVATAR&#x60; - User Avatar * &#x60;USER_COVER&#x60; - User Cover | 

## Example

```python
from plane.models.user_asset_upload import UserAssetUpload

# TODO update the JSON string below
json = "{}"
# create an instance of UserAssetUpload from a JSON string
user_asset_upload_instance = UserAssetUpload.from_json(json)
# print the JSON string representation of the object
print UserAssetUpload.to_json()

# convert the object into a dict
user_asset_upload_dict = user_asset_upload_instance.to_dict()
# create an instance of UserAssetUpload from a dict
user_asset_upload_from_dict = UserAssetUpload.from_dict(user_asset_upload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


