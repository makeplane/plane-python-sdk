# plane.CyclesApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_cycle_issues**](CyclesApi.md#add_cycle_issues) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | Add cycle issues
[**archive_cycle**](CyclesApi.md#archive_cycle) | **POST** /workspaces/{slug}/projects/{project_id}/archived-cycles/ | Archive cycle
[**archive_cycle2**](CyclesApi.md#archive_cycle2) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/archive/ | Archive cycle
[**create_cycle**](CyclesApi.md#create_cycle) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/ | Create cycle
[**delete_cycle**](CyclesApi.md#delete_cycle) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | Delete cycle
[**delete_cycle_issue**](CyclesApi.md#delete_cycle_issue) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | Delete cycle issue
[**get_cycle_issues**](CyclesApi.md#get_cycle_issues) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | Get cycle issues
[**get_cycle_issues2**](CyclesApi.md#get_cycle_issues2) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | Get cycle issues
[**get_cycles**](CyclesApi.md#get_cycles) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/ | Get cycles
[**get_cycles2**](CyclesApi.md#get_cycles2) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | Get cycles
[**transfer_cycle_issues**](CyclesApi.md#transfer_cycle_issues) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/transfer-issues/ | Transfer issues to a new cycle
[**unarchive_cycle**](CyclesApi.md#unarchive_cycle) | **DELETE** /workspaces/{slug}/projects/{project_id}/archived-cycles/{id}/unarchive/ | Unarchive cycle
[**update_cycle**](CyclesApi.md#update_cycle) | **PATCH** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | Update cycle


# **add_cycle_issues**
> CycleIssue add_cycle_issues(cycle_id, project_id, slug, add_cycle_issues_request=add_cycle_issues_request)

Add cycle issues

Add cycle issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.add_cycle_issues_request import AddCycleIssuesRequest
from plane.models.cycle_issue import CycleIssue
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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    add_cycle_issues_request = plane.AddCycleIssuesRequest() # AddCycleIssuesRequest |  (optional)

    try:
        # Add cycle issues
        api_response = api_instance.add_cycle_issues(cycle_id, project_id, slug, add_cycle_issues_request=add_cycle_issues_request)
        print("The response of CyclesApi->add_cycle_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->add_cycle_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **add_cycle_issues_request** | [**AddCycleIssuesRequest**](AddCycleIssuesRequest.md)|  | [optional] 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cycle issues added |  -  |
**400** | Issues are required |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **archive_cycle**
> archive_cycle(project_id, slug)

Archive cycle

Archive cycle

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
    api_instance = plane.CyclesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Archive cycle
        api_instance.archive_cycle(project_id, slug)
    except Exception as e:
        print("Exception when calling CyclesApi->archive_cycle: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

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
**204** | Cycle archived |  -  |
**400** | Cycle cannot be archived |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **archive_cycle2**
> archive_cycle2(cycle_id, project_id, slug)

Archive cycle

Archive cycle

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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Archive cycle
        api_instance.archive_cycle2(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling CyclesApi->archive_cycle2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

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
**204** | Cycle archived |  -  |
**400** | Cycle cannot be archived |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_cycle**
> Cycle create_cycle(project_id, slug, create_cycle_request=create_cycle_request)

Create cycle

Create cycle

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_cycle_request import CreateCycleRequest
from plane.models.cycle import Cycle
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
    api_instance = plane.CyclesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_cycle_request = plane.CreateCycleRequest() # CreateCycleRequest |  (optional)

    try:
        # Create cycle
        api_response = api_instance.create_cycle(project_id, slug, create_cycle_request=create_cycle_request)
        print("The response of CyclesApi->create_cycle:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->create_cycle: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_cycle_request** | [**CreateCycleRequest**](CreateCycleRequest.md)|  | [optional] 

### Return type

[**Cycle**](Cycle.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Cycle created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cycle**
> delete_cycle(id, project_id, slug)

Delete cycle

Delete cycle

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
    api_instance = plane.CyclesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete cycle
        api_instance.delete_cycle(id, project_id, slug)
    except Exception as e:
        print("Exception when calling CyclesApi->delete_cycle: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

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
**204** | Cycle deleted |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_cycle_issue**
> delete_cycle_issue(cycle_id, issue_id, project_id, slug)

Delete cycle issue

Delete cycle issue

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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete cycle issue
        api_instance.delete_cycle_issue(cycle_id, issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling CyclesApi->delete_cycle_issue: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

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
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cycle_issues**
> CycleIssue get_cycle_issues(cycle_id, project_id, slug)

Get cycle issues

Get cycle issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get cycle issues
        api_response = api_instance.get_cycle_issues(cycle_id, project_id, slug)
        print("The response of CyclesApi->get_cycle_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->get_cycle_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cycle_issues2**
> CycleIssue get_cycle_issues2(cycle_id, issue_id, project_id, slug)

Get cycle issues

Get cycle issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get cycle issues
        api_response = api_instance.get_cycle_issues2(cycle_id, issue_id, project_id, slug)
        print("The response of CyclesApi->get_cycle_issues2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->get_cycle_issues2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cycles**
> Cycle get_cycles(project_id, slug)

Get cycles

Get cycles

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.cycle import Cycle
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
    api_instance = plane.CyclesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get cycles
        api_response = api_instance.get_cycles(project_id, slug)
        print("The response of CyclesApi->get_cycles:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->get_cycles: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cycles |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_cycles2**
> Cycle get_cycles2(id, project_id, slug)

Get cycles

Get cycles

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.cycle import Cycle
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
    api_instance = plane.CyclesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get cycles
        api_response = api_instance.get_cycles2(id, project_id, slug)
        print("The response of CyclesApi->get_cycles2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->get_cycles2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cycles |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **transfer_cycle_issues**
> TransferCycleIssues200Response transfer_cycle_issues(cycle_id, project_id, slug, request_body=request_body)

Transfer issues to a new cycle

Transfer issues from the current cycle to a new cycle

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.transfer_cycle_issues200_response import TransferCycleIssues200Response
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
    api_instance = plane.CyclesApi(api_client)
    cycle_id = 'cycle_id_example' # str | Cycle ID
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug
    request_body = None # Dict[str, object] |  (optional)

    try:
        # Transfer issues to a new cycle
        api_response = api_instance.transfer_cycle_issues(cycle_id, project_id, slug, request_body=request_body)
        print("The response of CyclesApi->transfer_cycle_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->transfer_cycle_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**| Cycle ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **request_body** | [**Dict[str, object]**](object.md)|  | [optional] 

### Return type

[**TransferCycleIssues200Response**](TransferCycleIssues200Response.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: type, required, properties
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issues transferred successfully |  -  |
**400** | Bad request |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unarchive_cycle**
> unarchive_cycle(id, project_id, slug)

Unarchive cycle

Unarchive cycle

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
    api_instance = plane.CyclesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Unarchive cycle
        api_instance.unarchive_cycle(id, project_id, slug)
    except Exception as e:
        print("Exception when calling CyclesApi->unarchive_cycle: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

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
**204** | Cycle unarchived |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Cycle not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_cycle**
> Cycle update_cycle(id, project_id, slug, update_cycle_request=update_cycle_request)

Update cycle

Update cycle

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.models.update_cycle_request import UpdateCycleRequest
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
    api_instance = plane.CyclesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    update_cycle_request = plane.UpdateCycleRequest() # UpdateCycleRequest |  (optional)

    try:
        # Update cycle
        api_response = api_instance.update_cycle(id, project_id, slug, update_cycle_request=update_cycle_request)
        print("The response of CyclesApi->update_cycle:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CyclesApi->update_cycle: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **update_cycle_request** | [**UpdateCycleRequest**](UpdateCycleRequest.md)|  | [optional] 

### Return type

[**Cycle**](Cycle.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Cycle updated |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

