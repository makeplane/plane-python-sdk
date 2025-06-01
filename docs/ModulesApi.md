# plane.ModulesApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_module_issues**](ModulesApi.md#add_module_issues) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | Add module issues
[**archive_module**](ModulesApi.md#archive_module) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{id}/archive/ | Archive module
[**create_module**](ModulesApi.md#create_module) | **POST** /workspaces/{slug}/projects/{project_id}/modules/ | Create module
[**delete_module**](ModulesApi.md#delete_module) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | Delete module
[**delete_module_issue**](ModulesApi.md#delete_module_issue) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | Delete module issue
[**get_archived_modules**](ModulesApi.md#get_archived_modules) | **GET** /workspaces/{slug}/projects/{project_id}/archived-modules/ | Get archived modules
[**get_module**](ModulesApi.md#get_module) | **GET** /workspaces/{slug}/projects/{project_id}/modules/ | Get module
[**get_module2**](ModulesApi.md#get_module2) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | Get module
[**get_module_issues**](ModulesApi.md#get_module_issues) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | Get module issues
[**unarchive_module**](ModulesApi.md#unarchive_module) | **DELETE** /workspaces/{slug}/projects/{project_id}/archived-modules/{id}/unarchive/ | Unarchive module
[**update_module**](ModulesApi.md#update_module) | **PATCH** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | Update module


# **add_module_issues**
> ModuleIssue add_module_issues(module_id, project_id, slug, add_cycle_issues_request=add_cycle_issues_request)

Add module issues

Add module issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.add_cycle_issues_request import AddCycleIssuesRequest
from plane.models.module_issue import ModuleIssue
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
    api_instance = plane.ModulesApi(api_client)
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    add_cycle_issues_request = plane.AddCycleIssuesRequest() # AddCycleIssuesRequest |  (optional)

    try:
        # Add module issues
        api_response = api_instance.add_module_issues(module_id, project_id, slug, add_cycle_issues_request=add_cycle_issues_request)
        print("The response of ModulesApi->add_module_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->add_module_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **add_cycle_issues_request** | [**AddCycleIssuesRequest**](AddCycleIssuesRequest.md)|  | [optional] 

### Return type

[**ModuleIssue**](ModuleIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Module issues added |  -  |
**400** | Invalid request |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **archive_module**
> archive_module(id, project_id, slug)

Archive module

Archive module

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
    api_instance = plane.ModulesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Archive module
        api_instance.archive_module(id, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->archive_module: %s\n" % e)
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
**204** | Module archived |  -  |
**400** | Invalid request |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Module not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_module**
> Module create_module(project_id, slug, create_module_request=create_module_request)

Create module

Create module

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_module_request import CreateModuleRequest
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_module_request = plane.CreateModuleRequest() # CreateModuleRequest |  (optional)

    try:
        # Create module
        api_response = api_instance.create_module(project_id, slug, create_module_request=create_module_request)
        print("The response of ModulesApi->create_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->create_module: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_module_request** | [**CreateModuleRequest**](CreateModuleRequest.md)|  | [optional] 

### Return type

[**Module**](Module.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Module created |  -  |
**400** | Invalid request |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_module**
> delete_module(id, project_id, slug)

Delete module

Delete module

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
    api_instance = plane.ModulesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete module
        api_instance.delete_module(id, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->delete_module: %s\n" % e)
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
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_module_issue**
> delete_module_issue(issue_id, module_id, project_id, slug)

Delete module issue

Delete module issue

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
    api_instance = plane.ModulesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete module issue
        api_instance.delete_module_issue(issue_id, module_id, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->delete_module_issue: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **module_id** | **str**|  | 
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
**204** | Module issue deleted |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Module issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_archived_modules**
> Module get_archived_modules(project_id, slug)

Get archived modules

Get archived modules

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get archived modules
        api_response = api_instance.get_archived_modules(project_id, slug)
        print("The response of ModulesApi->get_archived_modules:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->get_archived_modules: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Module**](Module.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Archived modules |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_module**
> Module get_module(project_id, slug)

Get module

Get modules

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get module
        api_response = api_instance.get_module(project_id, slug)
        print("The response of ModulesApi->get_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->get_module: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Module**](Module.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Module |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_module2**
> Module get_module2(id, project_id, slug)

Get module

Get modules

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get module
        api_response = api_instance.get_module2(id, project_id, slug)
        print("The response of ModulesApi->get_module2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->get_module2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Module**](Module.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Module |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_module_issues**
> Issue get_module_issues(module_id, project_id, slug)

Get module issues

Get module issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue import Issue
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
    api_instance = plane.ModulesApi(api_client)
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get module issues
        api_response = api_instance.get_module_issues(module_id, project_id, slug)
        print("The response of ModulesApi->get_module_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->get_module_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Module issues |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unarchive_module**
> unarchive_module(id, project_id, slug)

Unarchive module

Unarchive module

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
    api_instance = plane.ModulesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Unarchive module
        api_instance.unarchive_module(id, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->unarchive_module: %s\n" % e)
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
**204** | Module unarchived |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Module not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_module**
> Module update_module(id, project_id, slug, create_module_request=create_module_request)

Update module

Update module

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_module_request import CreateModuleRequest
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_module_request = plane.CreateModuleRequest() # CreateModuleRequest |  (optional)

    try:
        # Update module
        api_response = api_instance.update_module(id, project_id, slug, create_module_request=create_module_request)
        print("The response of ModulesApi->update_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->update_module: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_module_request** | [**CreateModuleRequest**](CreateModuleRequest.md)|  | [optional] 

### Return type

[**Module**](Module.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

