# plane.ModulesApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_module_work_items**](ModulesApi.md#add_module_work_items) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | Add Work Items to Module
[**archive_module**](ModulesApi.md#archive_module) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/archive/ | Archive module
[**create_module**](ModulesApi.md#create_module) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/ | Create module
[**delete_module**](ModulesApi.md#delete_module) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Delete module
[**delete_module_work_item**](ModulesApi.md#delete_module_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | Delete module work item
[**list_archived_modules**](ModulesApi.md#list_archived_modules) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/archived-modules/ | List archived modules
[**list_module_work_items**](ModulesApi.md#list_module_work_items) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | List module work items
[**list_modules**](ModulesApi.md#list_modules) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/ | List modules
[**retrieve_module**](ModulesApi.md#retrieve_module) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Retrieve module
[**unarchive_module**](ModulesApi.md#unarchive_module) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/archived-modules/{pk}/unarchive/ | Unarchive module
[**update_module**](ModulesApi.md#update_module) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Update module


# **add_module_work_items**
> ModuleIssue add_module_work_items(module_id, project_id, slug, module_issue_request_request)

Add Work Items to Module

Assign multiple work items to a module or move them from another module. Automatically handles bulk creation and updates with activity tracking.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.module_issue import ModuleIssue
from plane.models.module_issue_request_request import ModuleIssueRequestRequest
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
    api_instance = plane.ModulesApi(api_client)
    module_id = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    module_issue_request_request = {"issues":["0ec6cfa4-e906-4aad-9390-2df0303a41cd","0ec6cfa4-e906-4aad-9390-2df0303a41ce"]} # ModuleIssueRequestRequest | 

    try:
        # Add Work Items to Module
        api_response = api_instance.add_module_work_items(module_id, project_id, slug, module_issue_request_request)
        print("The response of ModulesApi->add_module_work_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->add_module_work_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**| Module ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **module_issue_request_request** | [**ModuleIssueRequestRequest**](ModuleIssueRequestRequest.md)|  | 

### Return type

[**ModuleIssue**](ModuleIssue.md)

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
**404** | Module not found |  -  |
**200** | Module issues added |  -  |
**400** | Required fields are missing |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **archive_module**
> archive_module(pk, project_id, slug)

Archive module

Move a module to archived status for historical tracking.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
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
    api_instance = plane.ModulesApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Archive module
        api_instance.archive_module(pk, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->archive_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Module ID | 
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
**404** | Module not found |  -  |
**204** | Resource archived successfully |  -  |
**400** | Resource cannot be archived in current state |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_module**
> Module create_module(project_id, slug, module_create_request)

Create module

Create a new project module with specified name, description, and timeline.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.module import Module
from plane.models.module_create_request import ModuleCreateRequest
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
    api_instance = plane.ModulesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    module_create_request = {"name":"New Module","description":"New module description","start_date":"2021-01-01","end_date":"2021-01-31","external_id":"1234567890","external_source":"github"} # ModuleCreateRequest | 

    try:
        # Create module
        api_response = api_instance.create_module(project_id, slug, module_create_request)
        print("The response of ModulesApi->create_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->create_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **module_create_request** | [**ModuleCreateRequest**](ModuleCreateRequest.md)|  | 

### Return type

[**Module**](Module.md)

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
**404** | Project not found |  -  |
**201** | Module created |  -  |
**400** | Invalid request data provided |  -  |
**409** | Resource with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_module**
> delete_module(pk, project_id, slug)

Delete module

Permanently remove a module and all its associated issue relationships.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
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
    api_instance = plane.ModulesApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete module
        api_instance.delete_module(pk, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->delete_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Module ID | 
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
**403** | Only admin or creator can perform this action |  -  |
**404** | Module not found |  -  |
**204** | Resource deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_module_work_item**
> delete_module_work_item(issue_id, module_id, project_id, slug)

Delete module work item

Remove a work item from a module while keeping the work item in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
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
    api_instance = plane.ModulesApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    module_id = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete module work item
        api_instance.delete_module_work_item(issue_id, module_id, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->delete_module_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **module_id** | **str**| Module ID | 
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
**404** | Module issue not found |  -  |
**204** | Resource deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_archived_modules**
> PaginatedArchivedModuleResponse list_archived_modules(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

List archived modules

Retrieve all modules that have been archived in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_archived_module_response import PaginatedArchivedModuleResponse
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
    api_instance = plane.ModulesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List archived modules
        api_response = api_instance.list_archived_modules(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of ModulesApi->list_archived_modules:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->list_archived_modules: %s\n" % e)
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

[**PaginatedArchivedModuleResponse**](PaginatedArchivedModuleResponse.md)

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
**200** | Paginated list of archived modules |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_module_work_items**
> PaginatedModuleIssueResponse list_module_work_items(module_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

List module work items

Retrieve all work items assigned to a module with detailed information.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_module_issue_response import PaginatedModuleIssueResponse
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
    api_instance = plane.ModulesApi(api_client)
    module_id = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List module work items
        api_response = api_instance.list_module_work_items(module_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of ModulesApi->list_module_work_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->list_module_work_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**| Module ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedModuleIssueResponse**](PaginatedModuleIssueResponse.md)

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
**404** | Module not found |  -  |
**200** | Paginated list of module work items |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_modules**
> PaginatedModuleResponse list_modules(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

List modules

Retrieve all modules in a project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_module_response import PaginatedModuleResponse
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
    api_instance = plane.ModulesApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List modules
        api_response = api_instance.list_modules(project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of ModulesApi->list_modules:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->list_modules: %s\n" % e)
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

[**PaginatedModuleResponse**](PaginatedModuleResponse.md)

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
**404** | Module not found |  -  |
**200** | Paginated list of modules |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_module**
> Module retrieve_module(pk, project_id, slug)

Retrieve module

Retrieve details of a specific module.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.module import Module
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
    api_instance = plane.ModulesApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Retrieve module
        api_response = api_instance.retrieve_module(pk, project_id, slug)
        print("The response of ModulesApi->retrieve_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->retrieve_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Module ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**Module**](Module.md)

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
**404** | Module not found |  -  |
**200** | Module |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **unarchive_module**
> unarchive_module(pk, project_id, slug)

Unarchive module

Restore an archived module to active status, making it available for regular use.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
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
    api_instance = plane.ModulesApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Unarchive module
        api_instance.unarchive_module(pk, project_id, slug)
    except Exception as e:
        print("Exception when calling ModulesApi->unarchive_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Module ID | 
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
**404** | Module not found |  -  |
**204** | Resource unarchived successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_module**
> Module update_module(pk, project_id, slug, patched_module_update_request=patched_module_update_request)

Update module

Modify an existing module's properties like name, description, status, or timeline.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.module import Module
from plane.models.patched_module_update_request import PatchedModuleUpdateRequest
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
    api_instance = plane.ModulesApi(api_client)
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Module ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    patched_module_update_request = {"name":"Updated Module","description":"Updated module description","start_date":"2021-01-01","end_date":"2021-01-31","external_id":"1234567890","external_source":"github"} # PatchedModuleUpdateRequest |  (optional)

    try:
        # Update module
        api_response = api_instance.update_module(pk, project_id, slug, patched_module_update_request=patched_module_update_request)
        print("The response of ModulesApi->update_module:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ModulesApi->update_module: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**| Module ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **patched_module_update_request** | [**PatchedModuleUpdateRequest**](PatchedModuleUpdateRequest.md)|  | [optional] 

### Return type

[**Module**](Module.md)

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
**404** | Module not found |  -  |
**200** | Module updated successfully |  -  |
**400** | Invalid request data |  -  |
**409** | Module with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

