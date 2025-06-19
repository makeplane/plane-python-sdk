# plane.AssetsApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_generic_asset_upload**](AssetsApi.md#create_generic_asset_upload) | **POST** /api/v1/workspaces/{slug}/assets/ | Generate presigned URL for generic asset upload
[**create_user_asset_upload**](AssetsApi.md#create_user_asset_upload) | **POST** /api/v1/assets/user-assets/ | Generate presigned URL for user asset upload
[**delete_user_asset**](AssetsApi.md#delete_user_asset) | **DELETE** /api/v1/assets/user-assets/{asset_id}/ | Delete user asset
[**get_generic_asset**](AssetsApi.md#get_generic_asset) | **GET** /api/v1/workspaces/{slug}/assets/{asset_id}/ | Get presigned URL for asset download
[**update_generic_asset**](AssetsApi.md#update_generic_asset) | **PATCH** /api/v1/workspaces/{slug}/assets/{asset_id}/ | Update generic asset after upload completion
[**update_user_asset**](AssetsApi.md#update_user_asset) | **PATCH** /api/v1/assets/user-assets/{asset_id}/ | Mark user asset as uploaded


# **create_generic_asset_upload**
> create_generic_asset_upload(slug, generic_asset_upload_request)

Generate presigned URL for generic asset upload

Generate presigned URL for generic asset upload

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.generic_asset_upload_request import GenericAssetUploadRequest
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    slug = 'my-workspace' # str | Workspace slug
    generic_asset_upload_request = {"name":"image.jpg","type":"image/jpeg","size":1024000,"project_id":"123e4567-e89b-12d3-a456-426614174000","external_id":"1234567890","external_source":"github"} # GenericAssetUploadRequest | 

    try:
        # Generate presigned URL for generic asset upload
        api_instance.create_generic_asset_upload(slug, generic_asset_upload_request)
    except Exception as e:
        print("Exception when calling AssetsApi->create_generic_asset_upload: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**| Workspace slug | 
 **generic_asset_upload_request** | [**GenericAssetUploadRequest**](GenericAssetUploadRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error |  -  |
**404** | The requested resource was not found. |  -  |
**409** | Asset with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_asset_upload**
> create_user_asset_upload(user_asset_upload_request)

Generate presigned URL for user asset upload

Generate presigned URL for user asset upload

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.user_asset_upload_request import UserAssetUploadRequest
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    user_asset_upload_request = {"name":"profile.jpg","type":"image/jpeg","size":1024000,"entity_type":"USER_AVATAR"} # UserAssetUploadRequest | 

    try:
        # Generate presigned URL for user asset upload
        api_instance.create_user_asset_upload(user_asset_upload_request)
    except Exception as e:
        print("Exception when calling AssetsApi->create_user_asset_upload: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_asset_upload_request** | [**UserAssetUploadRequest**](UserAssetUploadRequest.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error occurred with the provided data. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_asset**
> delete_user_asset(asset_id)

Delete user asset

Delete user asset.

Delete a user profile asset (avatar or cover image) and remove its reference from the user profile.
This performs a soft delete by marking the asset as deleted and updating the user's profile.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = '550e8400-e29b-41d4-a716-446655440000' # str | Asset ID

    try:
        # Delete user asset
        api_instance.delete_user_asset(asset_id)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_user_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| Asset ID | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**204** | Asset deleted successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_generic_asset**
> get_generic_asset(asset_id, slug)

Get presigned URL for asset download

Get presigned URL for asset download

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | 
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Get presigned URL for asset download
        api_instance.get_generic_asset(asset_id, slug)
    except Exception as e:
        print("Exception when calling AssetsApi->get_generic_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**|  | 
 **slug** | **str**| Workspace slug | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**200** | Presigned download URL generated successfully |  -  |
**400** | Bad request |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_generic_asset**
> update_generic_asset(asset_id, slug, patched_generic_asset_update_request=patched_generic_asset_update_request)

Update generic asset after upload completion

Update generic asset after upload completion

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.patched_generic_asset_update_request import PatchedGenericAssetUpdateRequest
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = '550e8400-e29b-41d4-a716-446655440000' # str | Asset ID
    slug = 'my-workspace' # str | Workspace slug
    patched_generic_asset_update_request = {"is_uploaded":true} # PatchedGenericAssetUpdateRequest |  (optional)

    try:
        # Update generic asset after upload completion
        api_instance.update_generic_asset(asset_id, slug, patched_generic_asset_update_request=patched_generic_asset_update_request)
    except Exception as e:
        print("Exception when calling AssetsApi->update_generic_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| Asset ID | 
 **slug** | **str**| Workspace slug | 
 **patched_generic_asset_update_request** | [**PatchedGenericAssetUpdateRequest**](PatchedGenericAssetUpdateRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**204** | Asset updated successfully |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_asset**
> update_user_asset(asset_id, patched_asset_update_request=patched_asset_update_request)

Mark user asset as uploaded

Mark user asset as uploaded

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.patched_asset_update_request import PatchedAssetUpdateRequest
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://api.plane.so
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "https://api.plane.so"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

configuration.access_token = os.environ["ACCESS_TOKEN"]

configuration.access_token = os.environ["ACCESS_TOKEN"]

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = '550e8400-e29b-41d4-a716-446655440000' # str | Asset ID
    patched_asset_update_request = {"attributes":{"name":"updated_profile.jpg","type":"image/jpeg","size":1024000},"entity_type":"USER_AVATAR"} # PatchedAssetUpdateRequest |  (optional)

    try:
        # Mark user asset as uploaded
        api_instance.update_user_asset(asset_id, patched_asset_update_request=patched_asset_update_request)
    except Exception as e:
        print("Exception when calling AssetsApi->update_user_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| Asset ID | 
 **patched_asset_update_request** | [**PatchedAssetUpdateRequest**](PatchedAssetUpdateRequest.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**204** | Asset updated successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

