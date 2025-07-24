# plane.WorkItemTypesApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_issue_type**](WorkItemTypesApi.md#create_issue_type) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/ | Create a new issue type
[**delete_issue_type**](WorkItemTypesApi.md#delete_issue_type) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Delete an issue type
[**list_issue_types**](WorkItemTypesApi.md#list_issue_types) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/ | List issue types
[**retrieve_issue_type**](WorkItemTypesApi.md#retrieve_issue_type) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Retrieve an issue type by id
[**update_issue_type**](WorkItemTypesApi.md#update_issue_type) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Update an issue type


# **create_issue_type**
> IssueTypeAPI create_issue_type(project_id, slug, issue_type_api_request)

Create a new issue type

Create a new issue type for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.models.issue_type_api_request import IssueTypeAPIRequest
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
    api_instance = plane.WorkItemTypesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_type_api_request = {"name":"Bug","description":"A bug is a problem with the software that prevents it from working as expected.","external_id":"1234567890","external_source":"github"} # IssueTypeAPIRequest | 

    try:
        # Create a new issue type
        api_response = api_instance.create_issue_type(project_id, slug, issue_type_api_request)
        print("The response of WorkItemTypesApi->create_issue_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemTypesApi->create_issue_type: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_type_api_request** | [**IssueTypeAPIRequest**](IssueTypeAPIRequest.md)|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

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
**201** | Issue type created |  -  |
**409** | Issue type with the same external id and external source already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_type**
> delete_issue_type(project_id, slug, type_id)

Delete an issue type

Delete an issue type

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
    api_instance = plane.WorkItemTypesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    type_id = 'type_id_example' # str | 

    try:
        # Delete an issue type
        api_instance.delete_issue_type(project_id, slug, type_id)
    except Exception as e:
        print("Exception when calling WorkItemTypesApi->delete_issue_type: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**|  | 

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
**404** | The requested resource was not found. |  -  |
**204** | Issue type deleted |  -  |
**400** | Default work item type cannot be deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issue_types**
> List[IssueTypeAPI] list_issue_types(project_id, slug)

List issue types

List all issue types for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
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
    api_instance = plane.WorkItemTypesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List issue types
        api_response = api_instance.list_issue_types(project_id, slug)
        print("The response of WorkItemTypesApi->list_issue_types:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemTypesApi->list_issue_types: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[IssueTypeAPI]**](IssueTypeAPI.md)

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
**404** | Issue type not found |  -  |
**200** | Issue types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_issue_type**
> IssueTypeAPI retrieve_issue_type(project_id, slug, type_id)

Retrieve an issue type by id

Retrieve an issue type by id

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
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
    api_instance = plane.WorkItemTypesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    type_id = 'type_id_example' # str | 

    try:
        # Retrieve an issue type by id
        api_response = api_instance.retrieve_issue_type(project_id, slug, type_id)
        print("The response of WorkItemTypesApi->retrieve_issue_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemTypesApi->retrieve_issue_type: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

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
**404** | Issue type not found |  -  |
**200** | Issue types |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_type**
> IssueTypeAPI update_issue_type(project_id, slug, type_id, patched_issue_type_api_request=patched_issue_type_api_request)

Update an issue type

Update an issue type

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.models.patched_issue_type_api_request import PatchedIssueTypeAPIRequest
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
    api_instance = plane.WorkItemTypesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    type_id = 'type_id_example' # str | 
    patched_issue_type_api_request = {"name":"Bug","description":"A bug is a problem with the software that prevents it from working as expected.","external_id":"1234567890","external_source":"github"} # PatchedIssueTypeAPIRequest |  (optional)

    try:
        # Update an issue type
        api_response = api_instance.update_issue_type(project_id, slug, type_id, patched_issue_type_api_request=patched_issue_type_api_request)
        print("The response of WorkItemTypesApi->update_issue_type:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemTypesApi->update_issue_type: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**|  | 
 **patched_issue_type_api_request** | [**PatchedIssueTypeAPIRequest**](PatchedIssueTypeAPIRequest.md)|  | [optional] 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

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
**200** | Issue type updated |  -  |
**409** | Issue type with the same external id and external source already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

