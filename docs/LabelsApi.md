# plane.LabelsApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_label**](LabelsApi.md#create_label) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/labels/ | Endpoints for label create/update/delete and fetch label details
[**delete_label**](LabelsApi.md#delete_label) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Delete a label
[**get_labels**](LabelsApi.md#get_labels) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Endpoints for label create/update/delete and fetch label details
[**list_labels**](LabelsApi.md#list_labels) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/labels/ | Endpoints for label create/update/delete and fetch label details
[**update_label**](LabelsApi.md#update_label) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Update a label


# **create_label**
> Label create_label(project_id, slug, label_create_update_request)

Endpoints for label create/update/delete and fetch label details

Create a new label in the specified project with name, color, and description.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.label import Label
from plane.models.label_create_update_request import LabelCreateUpdateRequest
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
    api_instance = plane.LabelsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    label_create_update_request = {"name":"New Label","color":"#ff0000","description":"New label description","external_id":"1234567890","external_source":"github"} # LabelCreateUpdateRequest | 

    try:
        # Endpoints for label create/update/delete and fetch label details
        api_response = api_instance.create_label(project_id, slug, label_create_update_request)
        print("The response of LabelsApi->create_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->create_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **label_create_update_request** | [**LabelCreateUpdateRequest**](LabelCreateUpdateRequest.md)|  | 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | The requested resource was not found. |  -  |
**201** | Label created successfully |  -  |
**400** | Invalid request data provided |  -  |
**409** | Label with the same name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_label**
> delete_label(pk, project_id, slug)

Delete a label

Permanently remove a label from the project. This action cannot be undone.

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
    api_instance = plane.LabelsApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Label ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete a label
        api_instance.delete_label(pk, project_id, slug)
    except Exception as e:
        print("Exception when calling LabelsApi->delete_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Label ID | 
 **project_id** | **str**| Project ID | 
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
**404** | Label not found |  -  |
**204** | Resource deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_labels**
> Label get_labels(pk, project_id, slug)

Endpoints for label create/update/delete and fetch label details

Retrieve details of a specific label.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.label import Label
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
    api_instance = plane.LabelsApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Label ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Endpoints for label create/update/delete and fetch label details
        api_response = api_instance.get_labels(pk, project_id, slug)
        print("The response of LabelsApi->get_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->get_labels: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Label ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Label not found |  -  |
**200** | Labels |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_labels**
> PaginatedLabelResponse list_labels(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

Endpoints for label create/update/delete and fetch label details

Retrieve all labels in a project. Supports filtering by name and color.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.paginated_label_response import PaginatedLabelResponse
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
    api_instance = plane.LabelsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # Endpoints for label create/update/delete and fetch label details
        api_response = api_instance.list_labels(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of LabelsApi->list_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->list_labels: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedLabelResponse**](PaginatedLabelResponse.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |
**200** | Paginated list of labels |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_label**
> Label update_label(pk, project_id, slug, patched_label_create_update_request=patched_label_create_update_request)

Update a label

Partially update an existing label's properties like name, color, or description.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.label import Label
from plane.models.patched_label_create_update_request import PatchedLabelCreateUpdateRequest
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
    api_instance = plane.LabelsApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Label ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    patched_label_create_update_request = {"name":"Updated Label","color":"#00ff00","description":"Updated label description","external_id":"1234567890","external_source":"github"} # PatchedLabelCreateUpdateRequest |  (optional)

    try:
        # Update a label
        api_response = api_instance.update_label(pk, project_id, slug, patched_label_create_update_request=patched_label_create_update_request)
        print("The response of LabelsApi->update_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->update_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Label ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **patched_label_create_update_request** | [**PatchedLabelCreateUpdateRequest**](PatchedLabelCreateUpdateRequest.md)|  | [optional] 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Label not found |  -  |
**200** | Label updated successfully |  -  |
**400** | Invalid request data provided |  -  |
**409** | Resource with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

