# plane.WorkItemsApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_work_item**](WorkItemsApi.md#create_work_item) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/ | Create work item
[**create_work_item_relation**](WorkItemsApi.md#create_work_item_relation) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/relations/ | Create work item relation
[**delete_work_item**](WorkItemsApi.md#delete_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Delete work item
[**get_workspace_work_item**](WorkItemsApi.md#get_workspace_work_item) | **GET** /api/v1/workspaces/{slug}/issues/{project_identifier}-{issue_identifier}/ | Retrieve work item by identifiers
[**list_work_item_relations**](WorkItemsApi.md#list_work_item_relations) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/relations/ | List work item relations
[**list_work_items**](WorkItemsApi.md#list_work_items) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/ | List work items
[**remove_work_item_relation**](WorkItemsApi.md#remove_work_item_relation) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/relations/remove/ | Remove work item relation
[**retrieve_work_item**](WorkItemsApi.md#retrieve_work_item) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Retrieve work item
[**search_work_items**](WorkItemsApi.md#search_work_items) | **GET** /api/v1/workspaces/{slug}/issues/search/ | 
[**update_work_item**](WorkItemsApi.md#update_work_item) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Partially update work item


# **create_work_item**
> Issue create_work_item(project_id, slug, issue_request)

Create work item

Create a new work item in the specified project with the provided details.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue import Issue
from plane.models.issue_request import IssueRequest
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
    api_instance = plane.WorkItemsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_request = {"name":"New Issue","description":"New issue description","priority":"medium","state":"0ec6cfa4-e906-4aad-9390-2df0303a41cd","assignees":["0ec6cfa4-e906-4aad-9390-2df0303a41cd"],"labels":["0ec6cfa4-e906-4aad-9390-2df0303a41ce"],"external_id":"1234567890","external_source":"github"} # IssueRequest | 

    try:
        # Create work item
        api_response = api_instance.create_work_item(project_id, slug, issue_request)
        print("The response of WorkItemsApi->create_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->create_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_request** | [**IssueRequest**](IssueRequest.md)|  | 

### Return type

[**Issue**](Issue.md)

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
**201** | Work Item created successfully |  -  |
**400** | Invalid request data provided |  -  |
**409** | Resource with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_work_item_relation**
> List[IssueRelation] create_work_item_relation(issue_id, project_id, slug, issue_relation_create_request)

Create work item relation

Create relationships between work items. Supports various relation types including blocking, blocked_by, duplicate, relates_to, start_before, start_after, finish_before, and finish_after.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_relation import IssueRelation
from plane.models.issue_relation_create_request import IssueRelationCreateRequest
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_relation_create_request = {"relation_type":"blocking","issues":["550e8400-e29b-41d4-a716-446655440000","550e8400-e29b-41d4-a716-446655440001"]} # IssueRelationCreateRequest | 

    try:
        # Create work item relation
        api_response = api_instance.create_work_item_relation(issue_id, project_id, slug, issue_relation_create_request)
        print("The response of WorkItemsApi->create_work_item_relation:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->create_work_item_relation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_relation_create_request** | [**IssueRelationCreateRequest**](IssueRelationCreateRequest.md)|  | 

### Return type

[**List[IssueRelation]**](IssueRelation.md)

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
**404** | Issue not found |  -  |
**201** | Work item relations created successfully |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_item**
> delete_work_item(pk, project_id, slug)

Delete work item

Permanently delete an existing work item from the project. Only admins or the item creator can perform this action.

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
    api_instance = plane.WorkItemsApi(api_client)
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete work item
        api_instance.delete_work_item(pk, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkItemsApi->delete_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**|  | 
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
**404** | Work item not found |  -  |
**204** | Resource deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_work_item**
> Issue get_workspace_work_item(issue_identifier, project_identifier, slug)

Retrieve work item by identifiers

Retrieve a specific work item using workspace slug, project identifier, and issue identifier.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue import Issue
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_identifier = 123 # int | Issue sequence ID (numeric identifier within project)
    project_identifier = 'PROJ' # str | Project identifier (unique string within workspace)
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Retrieve work item by identifiers
        api_response = api_instance.get_workspace_work_item(issue_identifier, project_identifier, slug)
        print("The response of WorkItemsApi->get_workspace_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_workspace_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_identifier** | **int**| Issue sequence ID (numeric identifier within project) | 
 **project_identifier** | **str**| Project identifier (unique string within workspace) | 
 **slug** | **str**| Workspace slug | 

### Return type

[**Issue**](Issue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Work item details |  -  |
**404** | Work item not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_work_item_relations**
> IssueRelationResponse list_work_item_relations(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

List work item relations

Retrieve all relationships for a work item including blocking, blocked_by, duplicate, relates_to, start_before, start_after, finish_before, and finish_after relations.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_relation_response import IssueRelationResponse
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List work item relations
        api_response = api_instance.list_work_item_relations(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of WorkItemsApi->list_work_item_relations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->list_work_item_relations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**IssueRelationResponse**](IssueRelationResponse.md)

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
**404** | Issue not found |  -  |
**200** | Work item relations grouped by relation type |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_work_items**
> PaginatedWorkItemResponse list_work_items(project_id, slug, cursor=cursor, expand=expand, external_id=external_id, external_source=external_source, fields=fields, order_by=order_by, per_page=per_page)

List work items

Retrieve a paginated list of all work items in a project. Supports filtering, ordering, and field selection through query parameters.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_work_item_response import PaginatedWorkItemResponse
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
    api_instance = plane.WorkItemsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    external_id = '1234567890' # str | External system identifier for filtering or lookup (optional)
    external_source = 'github' # str | External system source name for filtering or lookup (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List work items
        api_response = api_instance.list_work_items(project_id, slug, cursor=cursor, expand=expand, external_id=external_id, external_source=external_source, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of WorkItemsApi->list_work_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->list_work_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **external_id** | **str**| External system identifier for filtering or lookup | [optional] 
 **external_source** | **str**| External system source name for filtering or lookup | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedWorkItemResponse**](PaginatedWorkItemResponse.md)

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
**200** | Paginated list of work items |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **remove_work_item_relation**
> remove_work_item_relation(issue_id, project_id, slug, issue_relation_remove_request)

Remove work item relation

Remove a relationship between work items by specifying the related work item ID.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_relation_remove_request import IssueRelationRemoveRequest
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_relation_remove_request = {"related_issue":"550e8400-e29b-41d4-a716-446655440000"} # IssueRelationRemoveRequest | 

    try:
        # Remove work item relation
        api_instance.remove_work_item_relation(issue_id, project_id, slug, issue_relation_remove_request)
    except Exception as e:
        print("Exception when calling WorkItemsApi->remove_work_item_relation: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_relation_remove_request** | [**IssueRelationRemoveRequest**](IssueRelationRemoveRequest.md)|  | 

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
**404** | Work item relation not found |  -  |
**204** | Work item relation removed successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_work_item**
> IssueDetail retrieve_work_item(pk, project_id, slug, expand=expand, external_id=external_id, external_source=external_source, fields=fields, order_by=order_by)

Retrieve work item

Retrieve details of a specific work item.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_detail import IssueDetail
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
    api_instance = plane.WorkItemsApi(api_client)
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    external_id = '1234567890' # str | External system identifier for filtering or lookup (optional)
    external_source = 'github' # str | External system source name for filtering or lookup (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)

    try:
        # Retrieve work item
        api_response = api_instance.retrieve_work_item(pk, project_id, slug, expand=expand, external_id=external_id, external_source=external_source, fields=fields, order_by=order_by)
        print("The response of WorkItemsApi->retrieve_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->retrieve_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **external_id** | **str**| External system identifier for filtering or lookup | [optional] 
 **external_source** | **str**| External system source name for filtering or lookup | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 

### Return type

[**IssueDetail**](IssueDetail.md)

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
**404** | Work item not found |  -  |
**200** | List of issues or issue details |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_work_items**
> IssueSearch search_work_items(search, slug, limit=limit, project_id=project_id, workspace_search=workspace_search)

Perform semantic search across issue names, sequence IDs, and project identifiers.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_search import IssueSearch
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
    api_instance = plane.WorkItemsApi(api_client)
    search = 'bug fix' # str | Search query to filter results by name, description, or identifier
    slug = 'my-workspace' # str | Workspace slug
    limit = 10 # int | Maximum number of results to return (optional)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID for filtering results within a specific project (optional)
    workspace_search = 'false' # str | Whether to search across entire workspace or within specific project (optional)

    try:
        api_response = api_instance.search_work_items(search, slug, limit=limit, project_id=project_id, workspace_search=workspace_search)
        print("The response of WorkItemsApi->search_work_items:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->search_work_items: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Search query to filter results by name, description, or identifier | 
 **slug** | **str**| Workspace slug | 
 **limit** | **int**| Maximum number of results to return | [optional] 
 **project_id** | **str**| Project ID for filtering results within a specific project | [optional] 
 **workspace_search** | **str**| Whether to search across entire workspace or within specific project | [optional] 

### Return type

[**IssueSearch**](IssueSearch.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Work item search results |  -  |
**400** | Bad request - invalid search parameters |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_work_item**
> Issue update_work_item(pk, project_id, slug, patched_issue_request=patched_issue_request)

Partially update work item

Partially update an existing work item with the provided fields. Supports external ID validation to prevent conflicts.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue import Issue
from plane.models.patched_issue_request import PatchedIssueRequest
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
    api_instance = plane.WorkItemsApi(api_client)
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    patched_issue_request = {"name":"Updated Issue","description":"Updated issue description","priority":"medium","state":"0ec6cfa4-e906-4aad-9390-2df0303a41cd","assignees":["0ec6cfa4-e906-4aad-9390-2df0303a41cd"],"labels":["0ec6cfa4-e906-4aad-9390-2df0303a41ce"]} # PatchedIssueRequest |  (optional)

    try:
        # Partially update work item
        api_response = api_instance.update_work_item(pk, project_id, slug, patched_issue_request=patched_issue_request)
        print("The response of WorkItemsApi->update_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->update_work_item: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **patched_issue_request** | [**PatchedIssueRequest**](PatchedIssueRequest.md)|  | [optional] 

### Return type

[**Issue**](Issue.md)

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
**404** | Work item not found |  -  |
**200** | Work Item patched successfully |  -  |
**400** | Invalid request data provided |  -  |
**409** | Resource with same external ID already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

