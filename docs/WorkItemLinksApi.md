# plane.WorkItemLinksApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_work_item_link**](WorkItemLinksApi.md#create_work_item_link) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Endpoints for issue link create/update/delete and fetch issue link details
[**delete_work_item_link**](WorkItemLinksApi.md#delete_work_item_link) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Endpoints for issue link create/update/delete and fetch issue link details
[**list_work_item_links**](WorkItemLinksApi.md#list_work_item_links) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Endpoints for issue link create/update/delete and fetch issue link details
[**retrieve_work_item_link**](WorkItemLinksApi.md#retrieve_work_item_link) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Endpoints for issue link create/update/delete and fetch issue link details
[**update_issue_link**](WorkItemLinksApi.md#update_issue_link) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Update an issue link


# **create_work_item_link**
> IssueLink create_work_item_link(issue_id, project_id, slug, issue_link_create_request)

Endpoints for issue link create/update/delete and fetch issue link details

Add a new external link to a work item with URL, title, and metadata.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_link import IssueLink
from plane.models.issue_link_create_request import IssueLinkCreateRequest
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
    api_instance = plane.WorkItemLinksApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_link_create_request = {"url":"https://example.com","title":"Example Link"} # IssueLinkCreateRequest | 

    try:
        # Endpoints for issue link create/update/delete and fetch issue link details
        api_response = api_instance.create_work_item_link(issue_id, project_id, slug, issue_link_create_request)
        print("The response of WorkItemLinksApi->create_work_item_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemLinksApi->create_work_item_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_link_create_request** | [**IssueLinkCreateRequest**](IssueLinkCreateRequest.md)|  | 

### Return type

[**IssueLink**](IssueLink.md)

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
**201** | Work item link created successfully |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_item_link**
> delete_work_item_link(issue_id, pk, project_id, slug)

Endpoints for issue link create/update/delete and fetch issue link details

Permanently remove an external link from a work item.

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
    api_instance = plane.WorkItemLinksApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Link ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Endpoints for issue link create/update/delete and fetch issue link details
        api_instance.delete_work_item_link(issue_id, pk, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkItemLinksApi->delete_work_item_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Link ID | 
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
**404** | Work item link not found |  -  |
**204** | Work item link deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_work_item_links**
> PaginatedIssueLinkResponse list_work_item_links(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

Endpoints for issue link create/update/delete and fetch issue link details

Retrieve all links associated with a work item. Supports filtering by URL, title, and metadata.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_issue_link_response import PaginatedIssueLinkResponse
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
    api_instance = plane.WorkItemLinksApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # Endpoints for issue link create/update/delete and fetch issue link details
        api_response = api_instance.list_work_item_links(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of WorkItemLinksApi->list_work_item_links:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemLinksApi->list_work_item_links: %s\n" % e)
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

[**PaginatedIssueLinkResponse**](PaginatedIssueLinkResponse.md)

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
**200** | Paginated list of work item links |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_work_item_link**
> PaginatedIssueLinkDetailResponse retrieve_work_item_link(issue_id, pk, project_id, slug, cursor=cursor, expand=expand, fields=fields, per_page=per_page)

Endpoints for issue link create/update/delete and fetch issue link details

Retrieve details of a specific work item link.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_issue_link_detail_response import PaginatedIssueLinkDetailResponse
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
    api_instance = plane.WorkItemLinksApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Link ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # Endpoints for issue link create/update/delete and fetch issue link details
        api_response = api_instance.retrieve_work_item_link(issue_id, pk, project_id, slug, cursor=cursor, expand=expand, fields=fields, per_page=per_page)
        print("The response of WorkItemLinksApi->retrieve_work_item_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemLinksApi->retrieve_work_item_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Link ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedIssueLinkDetailResponse**](PaginatedIssueLinkDetailResponse.md)

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
**200** | Work item link details or paginated list |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_link**
> IssueLink update_issue_link(issue_id, pk, project_id, slug, patched_issue_link_update_request=patched_issue_link_update_request)

Update an issue link

Modify the URL, title, or metadata of an existing issue link.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.issue_link import IssueLink
from plane.models.patched_issue_link_update_request import PatchedIssueLinkUpdateRequest
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
    api_instance = plane.WorkItemLinksApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Link ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    patched_issue_link_update_request = {"url":"https://example.com","title":"Updated Link"} # PatchedIssueLinkUpdateRequest |  (optional)

    try:
        # Update an issue link
        api_response = api_instance.update_issue_link(issue_id, pk, project_id, slug, patched_issue_link_update_request=patched_issue_link_update_request)
        print("The response of WorkItemLinksApi->update_issue_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemLinksApi->update_issue_link: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Link ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **patched_issue_link_update_request** | [**PatchedIssueLinkUpdateRequest**](PatchedIssueLinkUpdateRequest.md)|  | [optional] 

### Return type

[**IssueLink**](IssueLink.md)

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
**404** | Link not found |  -  |
**200** | Issue link updated successfully |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

