# plane.WorkItemPropertiesApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_issue_property**](WorkItemPropertiesApi.md#create_issue_property) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | Create a new issue property
[**create_issue_property_option**](WorkItemPropertiesApi.md#create_issue_property_option) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | Create a new issue property option
[**create_issue_property_value**](WorkItemPropertiesApi.md#create_issue_property_value) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | Create/update an issue property value
[**delete_issue_property**](WorkItemPropertiesApi.md#delete_issue_property) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Delete an issue property
[**delete_issue_property_option**](WorkItemPropertiesApi.md#delete_issue_property_option) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Delete an issue property option
[**list_issue_properties**](WorkItemPropertiesApi.md#list_issue_properties) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | List issue properties
[**list_issue_property_options**](WorkItemPropertiesApi.md#list_issue_property_options) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | List issue property options
[**list_issue_property_values**](WorkItemPropertiesApi.md#list_issue_property_values) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | List issue property values
[**retrieve_issue_property**](WorkItemPropertiesApi.md#retrieve_issue_property) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Get issue property by id
[**retrieve_issue_property_option**](WorkItemPropertiesApi.md#retrieve_issue_property_option) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Get issue property option by id
[**update_issue_property**](WorkItemPropertiesApi.md#update_issue_property) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Update an issue property
[**update_issue_property_option**](WorkItemPropertiesApi.md#update_issue_property_option) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Update an issue property option


# **create_issue_property**
> IssuePropertyAPI create_issue_property(project_id, slug, type_id, issue_property_api_request)

Create a new issue property

Create a new issue property

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.models.issue_property_api_request import IssuePropertyAPIRequest
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    type_id = '550e8400-e29b-41d4-a716-446655440000' # str | Type ID
    issue_property_api_request = {"name":"Priority","description":"The priority of the issue","property_type":"OPTION","external_id":"1234567890","external_source":"github"} # IssuePropertyAPIRequest | 

    try:
        # Create a new issue property
        api_response = api_instance.create_issue_property(project_id, slug, type_id, issue_property_api_request)
        print("The response of WorkItemPropertiesApi->create_issue_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->create_issue_property: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**| Type ID | 
 **issue_property_api_request** | [**IssuePropertyAPIRequest**](IssuePropertyAPIRequest.md)|  | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

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
**201** | Issue property created |  -  |
**409** | Issue property with the same external id and external source already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_issue_property_option**
> IssuePropertyOptionAPI create_issue_property_option(project_id, property_id, slug, issue_property_option_api_request)

Create a new issue property option

Create a new issue property option

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.models.issue_property_option_api_request import IssuePropertyOptionAPIRequest
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug
    issue_property_option_api_request = {"name":"High","description":"The highest priority","external_id":"1234567890","external_source":"github"} # IssuePropertyOptionAPIRequest | 

    try:
        # Create a new issue property option
        api_response = api_instance.create_issue_property_option(project_id, property_id, slug, issue_property_option_api_request)
        print("The response of WorkItemPropertiesApi->create_issue_property_option:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->create_issue_property_option: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 
 **issue_property_option_api_request** | [**IssuePropertyOptionAPIRequest**](IssuePropertyOptionAPIRequest.md)|  | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

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
**201** | Issue property option created |  -  |
**400** | Issue Property type is not OPTION |  -  |
**409** | Issue Property with the same external id and external source already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_issue_property_value**
> IssuePropertyValueAPI create_issue_property_value(issue_id, project_id, property_id, slug, issue_property_value_api_request)

Create/update an issue property value

Create/update an issue property value

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_value_api import IssuePropertyValueAPI
from plane.models.issue_property_value_api_request import IssuePropertyValueAPIRequest
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug
    issue_property_value_api_request = {"values":[{"value":"1234567890","external_id":"1234567890","external_source":"github"}]} # IssuePropertyValueAPIRequest | 

    try:
        # Create/update an issue property value
        api_response = api_instance.create_issue_property_value(issue_id, project_id, property_id, slug, issue_property_value_api_request)
        print("The response of WorkItemPropertiesApi->create_issue_property_value:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->create_issue_property_value: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 
 **issue_property_value_api_request** | [**IssuePropertyValueAPIRequest**](IssuePropertyValueAPIRequest.md)|  | 

### Return type

[**IssuePropertyValueAPI**](IssuePropertyValueAPI.md)

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
**404** | Issue property not found |  -  |
**201** | Issue property value created |  -  |
**400** | Value is required |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_property**
> delete_issue_property(project_id, property_id, slug, type_id)

Delete an issue property

Delete an issue property

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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | 
    slug = 'my-workspace' # str | Workspace slug
    type_id = '550e8400-e29b-41d4-a716-446655440000' # str | Type ID

    try:
        # Delete an issue property
        api_instance.delete_issue_property(project_id, property_id, slug, type_id)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->delete_issue_property: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **property_id** | **str**|  | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**| Type ID | 

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
**204** | Issue property deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_property_option**
> delete_issue_property_option(option_id, project_id, property_id, slug)

Delete an issue property option

Delete an issue property option

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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete an issue property option
        api_instance.delete_issue_property_option(option_id, project_id, property_id, slug)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->delete_issue_property_option: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
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
**404** | Issue property option not found |  -  |
**204** | Issue property option deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issue_properties**
> List[IssuePropertyAPI] list_issue_properties(project_id, slug, type_id)

List issue properties

List issue properties

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    type_id = '550e8400-e29b-41d4-a716-446655440000' # str | Type ID

    try:
        # List issue properties
        api_response = api_instance.list_issue_properties(project_id, slug, type_id)
        print("The response of WorkItemPropertiesApi->list_issue_properties:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->list_issue_properties: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**| Type ID | 

### Return type

[**List[IssuePropertyAPI]**](IssuePropertyAPI.md)

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
**404** | The requested resource was not found. |  -  |
**200** | Issue properties |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issue_property_options**
> List[IssuePropertyOptionAPI] list_issue_property_options(project_id, property_id, slug)

List issue property options

List issue property options

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List issue property options
        api_response = api_instance.list_issue_property_options(project_id, property_id, slug)
        print("The response of WorkItemPropertiesApi->list_issue_property_options:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->list_issue_property_options: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[IssuePropertyOptionAPI]**](IssuePropertyOptionAPI.md)

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
**404** | Issue property not found |  -  |
**200** | Issue property options |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issue_property_values**
> List[IssuePropertyValueAPIDetail] list_issue_property_values(issue_id, project_id, property_id, slug)

List issue property values

List issue property values

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_value_api_detail import IssuePropertyValueAPIDetail
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List issue property values
        api_response = api_instance.list_issue_property_values(issue_id, project_id, property_id, slug)
        print("The response of WorkItemPropertiesApi->list_issue_property_values:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->list_issue_property_values: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[IssuePropertyValueAPIDetail]**](IssuePropertyValueAPIDetail.md)

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
**404** | The requested resource was not found. |  -  |
**200** | Issue property values |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_issue_property**
> IssuePropertyAPI retrieve_issue_property(project_id, property_id, slug, type_id)

Get issue property by id

Get issue property by id

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | 
    slug = 'my-workspace' # str | Workspace slug
    type_id = '550e8400-e29b-41d4-a716-446655440000' # str | Type ID

    try:
        # Get issue property by id
        api_response = api_instance.retrieve_issue_property(project_id, property_id, slug, type_id)
        print("The response of WorkItemPropertiesApi->retrieve_issue_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->retrieve_issue_property: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **property_id** | **str**|  | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**| Type ID | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

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
**404** | The requested resource was not found. |  -  |
**200** | Issue properties |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_issue_property_option**
> IssuePropertyOptionAPI retrieve_issue_property_option(option_id, project_id, property_id, slug)

Get issue property option by id

Get issue property option by id

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Get issue property option by id
        api_response = api_instance.retrieve_issue_property_option(option_id, project_id, property_id, slug)
        print("The response of WorkItemPropertiesApi->retrieve_issue_property_option:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->retrieve_issue_property_option: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

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
**404** | Issue property not found |  -  |
**200** | Issue property options |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_property**
> IssuePropertyAPI update_issue_property(project_id, property_id, slug, type_id, patched_issue_property_api_request=patched_issue_property_api_request)

Update an issue property

Update an issue property

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.models.patched_issue_property_api_request import PatchedIssuePropertyAPIRequest
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | 
    slug = 'my-workspace' # str | Workspace slug
    type_id = '550e8400-e29b-41d4-a716-446655440000' # str | Type ID
    patched_issue_property_api_request = {"name":"Priority","description":"The priority of the issue","property_type":"OPTION","external_id":"1234567890","external_source":"github"} # PatchedIssuePropertyAPIRequest |  (optional)

    try:
        # Update an issue property
        api_response = api_instance.update_issue_property(project_id, property_id, slug, type_id, patched_issue_property_api_request=patched_issue_property_api_request)
        print("The response of WorkItemPropertiesApi->update_issue_property:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->update_issue_property: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **property_id** | **str**|  | 
 **slug** | **str**| Workspace slug | 
 **type_id** | **str**| Type ID | 
 **patched_issue_property_api_request** | [**PatchedIssuePropertyAPIRequest**](PatchedIssuePropertyAPIRequest.md)|  | [optional] 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

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
**200** | Issue property updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_property_option**
> IssuePropertyOptionAPI update_issue_property_option(option_id, project_id, property_id, slug, patched_issue_property_option_api_request=patched_issue_property_option_api_request)

Update an issue property option

Update an issue property option

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.models.patched_issue_property_option_api_request import PatchedIssuePropertyOptionAPIRequest
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
    api_instance = plane.WorkItemPropertiesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    property_id = 'property_id_example' # str | Property ID
    slug = 'my-workspace' # str | Workspace slug
    patched_issue_property_option_api_request = {"name":"High","description":"The highest priority","external_id":"1234567890","external_source":"github"} # PatchedIssuePropertyOptionAPIRequest |  (optional)

    try:
        # Update an issue property option
        api_response = api_instance.update_issue_property_option(option_id, project_id, property_id, slug, patched_issue_property_option_api_request=patched_issue_property_option_api_request)
        print("The response of WorkItemPropertiesApi->update_issue_property_option:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemPropertiesApi->update_issue_property_option: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **property_id** | **str**| Property ID | 
 **slug** | **str**| Workspace slug | 
 **patched_issue_property_option_api_request** | [**PatchedIssuePropertyOptionAPIRequest**](PatchedIssuePropertyOptionAPIRequest.md)|  | [optional] 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

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
**404** | Issue property option not found |  -  |
**200** | Issue property option updated |  -  |
**400** | Default option already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

