# plane.AssetsApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_generic_asset_upload**](AssetsApi.md#create_generic_asset_upload) | **POST** /workspaces/{slug}/assets/ | Create Assets
[**create_generic_asset_upload2**](AssetsApi.md#create_generic_asset_upload2) | **POST** /workspaces/{slug}/assets/{asset_id}/ | Create Assets
[**create_user_asset_upload**](AssetsApi.md#create_user_asset_upload) | **POST** /assets/user-assets/ | Create User Assets
[**create_user_asset_upload2**](AssetsApi.md#create_user_asset_upload2) | **POST** /assets/user-assets/{asset_id}/ | Create User Assets
[**create_user_server_asset_upload**](AssetsApi.md#create_user_server_asset_upload) | **POST** /assets/user-assets/server/ | Create Server
[**create_user_server_asset_upload2**](AssetsApi.md#create_user_server_asset_upload2) | **POST** /assets/user-assets/{asset_id}/server/ | Create Server
[**delete_user_asset**](AssetsApi.md#delete_user_asset) | **DELETE** /assets/user-assets/ | Delete User Assets
[**delete_user_asset2**](AssetsApi.md#delete_user_asset2) | **DELETE** /assets/user-assets/{asset_id}/ | Delete User Assets
[**delete_user_server_asset**](AssetsApi.md#delete_user_server_asset) | **DELETE** /assets/user-assets/server/ | Delete Server
[**delete_user_server_asset2**](AssetsApi.md#delete_user_server_asset2) | **DELETE** /assets/user-assets/{asset_id}/server/ | Delete Server
[**get_generic_asset**](AssetsApi.md#get_generic_asset) | **GET** /workspaces/{slug}/assets/ | Retrieve Assets
[**get_generic_asset2**](AssetsApi.md#get_generic_asset2) | **GET** /workspaces/{slug}/assets/{asset_id}/ | Retrieve Assets
[**update_generic_asset**](AssetsApi.md#update_generic_asset) | **PATCH** /workspaces/{slug}/assets/ | Update Assets
[**update_generic_asset2**](AssetsApi.md#update_generic_asset2) | **PATCH** /workspaces/{slug}/assets/{asset_id}/ | Update Assets
[**update_user_asset**](AssetsApi.md#update_user_asset) | **PATCH** /assets/user-assets/ | Update User Assets
[**update_user_asset2**](AssetsApi.md#update_user_asset2) | **PATCH** /assets/user-assets/{asset_id}/ | Update User Assets
[**update_user_server_asset**](AssetsApi.md#update_user_server_asset) | **PATCH** /assets/user-assets/server/ | Update Server
[**update_user_server_asset2**](AssetsApi.md#update_user_server_asset2) | **PATCH** /assets/user-assets/{asset_id}/server/ | Update Server


# **create_generic_asset_upload**
> create_generic_asset_upload(slug, generic_asset_upload)

Create Assets

Generate presigned URL for generic asset upload.

Create a presigned URL for uploading generic assets that can be bound to entities like issues.
Supports various file types and includes external source tracking for integrations.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.generic_asset_upload import GenericAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    slug = 'my-workspace' # str | Workspace slug identifier
    generic_asset_upload = plane.GenericAssetUpload() # GenericAssetUpload | 

    try:
        # Create Assets
        api_instance.create_generic_asset_upload(slug, generic_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_generic_asset_upload: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**| Workspace slug identifier | 
 **generic_asset_upload** | [**GenericAssetUpload**](GenericAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error |  -  |
**404** | The requested resource was not found. |  -  |
**409** | Asset with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_generic_asset_upload2**
> create_generic_asset_upload2(asset_id, slug, generic_asset_upload)

Create Assets

Generate presigned URL for generic asset upload.

Create a presigned URL for uploading generic assets that can be bound to entities like issues.
Supports various file types and includes external source tracking for integrations.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.generic_asset_upload import GenericAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | 
    slug = 'my-workspace' # str | Workspace slug identifier
    generic_asset_upload = plane.GenericAssetUpload() # GenericAssetUpload | 

    try:
        # Create Assets
        api_instance.create_generic_asset_upload2(asset_id, slug, generic_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_generic_asset_upload2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**|  | 
 **slug** | **str**| Workspace slug identifier | 
 **generic_asset_upload** | [**GenericAssetUpload**](GenericAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error |  -  |
**404** | The requested resource was not found. |  -  |
**409** | Asset with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_asset_upload**
> create_user_asset_upload(user_asset_upload)

Create User Assets

Generate presigned URL for user asset upload.

Create a presigned URL for uploading user profile assets (avatar or cover image).
This endpoint generates the necessary credentials for direct S3 upload.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.user_asset_upload import UserAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    user_asset_upload = plane.UserAssetUpload() # UserAssetUpload | 

    try:
        # Create User Assets
        api_instance.create_user_asset_upload(user_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_user_asset_upload: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_asset_upload** | [**UserAssetUpload**](UserAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error occurred with the provided data. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_asset_upload2**
> create_user_asset_upload2(asset_id, user_asset_upload)

Create User Assets

Generate presigned URL for user asset upload.

Create a presigned URL for uploading user profile assets (avatar or cover image).
This endpoint generates the necessary credentials for direct S3 upload.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.user_asset_upload import UserAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | 
    user_asset_upload = plane.UserAssetUpload() # UserAssetUpload | 

    try:
        # Create User Assets
        api_instance.create_user_asset_upload2(asset_id, user_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_user_asset_upload2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**|  | 
 **user_asset_upload** | [**UserAssetUpload**](UserAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error occurred with the provided data. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_server_asset_upload**
> create_user_server_asset_upload(user_asset_upload)

Create Server

Generate presigned URL for user server asset upload.

Create a presigned URL for uploading user profile assets (avatar or cover image) using server credentials.
This endpoint generates the necessary credentials for direct S3 upload with server-side authentication.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.user_asset_upload import UserAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    user_asset_upload = plane.UserAssetUpload() # UserAssetUpload | 

    try:
        # Create Server
        api_instance.create_user_server_asset_upload(user_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_user_server_asset_upload: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **user_asset_upload** | [**UserAssetUpload**](UserAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error occurred with the provided data. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_user_server_asset_upload2**
> create_user_server_asset_upload2(asset_id, user_asset_upload)

Create Server

Generate presigned URL for user server asset upload.

Create a presigned URL for uploading user profile assets (avatar or cover image) using server credentials.
This endpoint generates the necessary credentials for direct S3 upload with server-side authentication.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.user_asset_upload import UserAssetUpload
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | 
    user_asset_upload = plane.UserAssetUpload() # UserAssetUpload | 

    try:
        # Create Server
        api_instance.create_user_server_asset_upload2(asset_id, user_asset_upload)
    except Exception as e:
        print("Exception when calling AssetsApi->create_user_server_asset_upload2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**|  | 
 **user_asset_upload** | [**UserAssetUpload**](UserAssetUpload.md)|  | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned URL generated successfully |  -  |
**400** | Validation error occurred with the provided data. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_asset**
> delete_user_asset(asset_id)

Delete User Assets

Delete user asset.

Delete a user profile asset (avatar or cover image) and remove its reference from the user profile.
This performs a soft delete by marking the asset as deleted and updating the user's profile.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset

    try:
        # Delete User Assets
        api_instance.delete_user_asset(asset_id)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_user_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset deleted successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_asset2**
> delete_user_asset2(asset_id)

Delete User Assets

Delete user asset.

Delete a user profile asset (avatar or cover image) and remove its reference from the user profile.
This performs a soft delete by marking the asset as deleted and updating the user's profile.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset

    try:
        # Delete User Assets
        api_instance.delete_user_asset2(asset_id)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_user_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset deleted successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_server_asset**
> delete_user_server_asset(asset_id)

Delete Server

Delete user server asset.

Delete a user profile asset (avatar or cover image) using server credentials and remove its reference from the user profile.
This performs a soft delete by marking the asset as deleted and updating the user's profile.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset

    try:
        # Delete Server
        api_instance.delete_user_server_asset(asset_id)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_user_server_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset deleted successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_user_server_asset2**
> delete_user_server_asset2(asset_id)

Delete Server

Delete user server asset.

Delete a user profile asset (avatar or cover image) using server credentials and remove its reference from the user profile.
This performs a soft delete by marking the asset as deleted and updating the user's profile.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset

    try:
        # Delete Server
        api_instance.delete_user_server_asset2(asset_id)
    except Exception as e:
        print("Exception when calling AssetsApi->delete_user_server_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset deleted successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_generic_asset**
> get_generic_asset(asset_id, slug)

Retrieve Assets

Get presigned URL for asset download.

Generate a presigned URL for downloading a generic asset.
The asset must be uploaded and associated with the specified workspace.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    slug = 'my-workspace' # str | Workspace slug identifier

    try:
        # Retrieve Assets
        api_instance.get_generic_asset(asset_id, slug)
    except Exception as e:
        print("Exception when calling AssetsApi->get_generic_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **slug** | **str**| Workspace slug identifier | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned download URL generated successfully |  -  |
**400** | Bad request |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_generic_asset2**
> get_generic_asset2(asset_id, slug)

Retrieve Assets

Get presigned URL for asset download.

Generate a presigned URL for downloading a generic asset.
The asset must be uploaded and associated with the specified workspace.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    slug = 'my-workspace' # str | Workspace slug identifier

    try:
        # Retrieve Assets
        api_instance.get_generic_asset2(asset_id, slug)
    except Exception as e:
        print("Exception when calling AssetsApi->get_generic_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **slug** | **str**| Workspace slug identifier | 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned download URL generated successfully |  -  |
**400** | Bad request |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_generic_asset**
> update_generic_asset(asset_id, slug, patched_generic_asset_update=patched_generic_asset_update)

Update Assets

Update generic asset after upload completion.

Update the asset status after the file has been uploaded to S3.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded
and trigger metadata extraction.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_generic_asset_update import PatchedGenericAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    slug = 'my-workspace' # str | Workspace slug identifier
    patched_generic_asset_update = plane.PatchedGenericAssetUpdate() # PatchedGenericAssetUpdate |  (optional)

    try:
        # Update Assets
        api_instance.update_generic_asset(asset_id, slug, patched_generic_asset_update=patched_generic_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_generic_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **slug** | **str**| Workspace slug identifier | 
 **patched_generic_asset_update** | [**PatchedGenericAssetUpdate**](PatchedGenericAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_generic_asset2**
> update_generic_asset2(asset_id, slug, patched_generic_asset_update=patched_generic_asset_update)

Update Assets

Update generic asset after upload completion.

Update the asset status after the file has been uploaded to S3.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded
and trigger metadata extraction.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_generic_asset_update import PatchedGenericAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    slug = 'my-workspace' # str | Workspace slug identifier
    patched_generic_asset_update = plane.PatchedGenericAssetUpdate() # PatchedGenericAssetUpdate |  (optional)

    try:
        # Update Assets
        api_instance.update_generic_asset2(asset_id, slug, patched_generic_asset_update=patched_generic_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_generic_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **slug** | **str**| Workspace slug identifier | 
 **patched_generic_asset_update** | [**PatchedGenericAssetUpdate**](PatchedGenericAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | Asset not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_asset**
> update_user_asset(asset_id, patched_asset_update=patched_asset_update)

Update User Assets

Update user asset after upload completion.

Update the asset status and attributes after the file has been uploaded to S3.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_asset_update import PatchedAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    patched_asset_update = plane.PatchedAssetUpdate() # PatchedAssetUpdate |  (optional)

    try:
        # Update User Assets
        api_instance.update_user_asset(asset_id, patched_asset_update=patched_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_user_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **patched_asset_update** | [**PatchedAssetUpdate**](PatchedAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_asset2**
> update_user_asset2(asset_id, patched_asset_update=patched_asset_update)

Update User Assets

Update user asset after upload completion.

Update the asset status and attributes after the file has been uploaded to S3.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_asset_update import PatchedAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    patched_asset_update = plane.PatchedAssetUpdate() # PatchedAssetUpdate |  (optional)

    try:
        # Update User Assets
        api_instance.update_user_asset2(asset_id, patched_asset_update=patched_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_user_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **patched_asset_update** | [**PatchedAssetUpdate**](PatchedAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_server_asset**
> update_user_server_asset(asset_id, patched_asset_update=patched_asset_update)

Update Server

Update user server asset after upload completion.

Update the asset status and attributes after the file has been uploaded to S3 using server credentials.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_asset_update import PatchedAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    patched_asset_update = plane.PatchedAssetUpdate() # PatchedAssetUpdate |  (optional)

    try:
        # Update Server
        api_instance.update_user_server_asset(asset_id, patched_asset_update=patched_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_user_server_asset: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **patched_asset_update** | [**PatchedAssetUpdate**](PatchedAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_user_server_asset2**
> update_user_server_asset2(asset_id, patched_asset_update=patched_asset_update)

Update Server

Update user server asset after upload completion.

Update the asset status and attributes after the file has been uploaded to S3 using server credentials.
This endpoint should be called after completing the S3 upload to mark the asset as uploaded.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.patched_asset_update import PatchedAssetUpdate
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to /api/v1
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "/api/v1"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuthentication
configuration.api_key['ApiKeyAuthentication'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuthentication'] = 'Bearer'

# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.AssetsApi(api_client)
    asset_id = 'asset_id_example' # str | UUID of the asset
    patched_asset_update = plane.PatchedAssetUpdate() # PatchedAssetUpdate |  (optional)

    try:
        # Update Server
        api_instance.update_user_server_asset2(asset_id, patched_asset_update=patched_asset_update)
    except Exception as e:
        print("Exception when calling AssetsApi->update_user_server_asset2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset_id** | **str**| UUID of the asset | 
 **patched_asset_update** | [**PatchedAssetUpdate**](PatchedAssetUpdate.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Asset updated successfully |  -  |
**404** | The requested resource was not found. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

