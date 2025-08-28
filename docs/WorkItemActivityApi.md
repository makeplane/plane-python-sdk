# plane.WorkItemActivityApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_work_item_activities**](WorkItemActivityApi.md#list_work_item_activities) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/ | Endpoints for issue activity/search and fetch issue activity details
[**retrieve_work_item_activity**](WorkItemActivityApi.md#retrieve_work_item_activity) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/{pk}/ | Endpoints for issue activity/search and fetch issue activity details


# **list_work_item_activities**
> PaginatedIssueActivityResponse list_work_item_activities(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

Endpoints for issue activity/search and fetch issue activity details

Retrieve all activities for a work item. Supports filtering by activity type and date range.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_issue_activity_response import PaginatedIssueActivityResponse
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
    api_instance = plane.WorkItemActivityApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # Endpoints for issue activity/search and fetch issue activity details
        api_response = api_instance.list_work_item_activities(issue_id, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of WorkItemActivityApi->list_work_item_activities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemActivityApi->list_work_item_activities: %s\n" % e)
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

[**PaginatedIssueActivityResponse**](PaginatedIssueActivityResponse.md)

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
**200** | Paginated list of issue activities |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_work_item_activity**
> PaginatedIssueActivityDetailResponse retrieve_work_item_activity(issue_id, pk, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)

Endpoints for issue activity/search and fetch issue activity details

Retrieve details of a specific activity.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_issue_activity_detail_response import PaginatedIssueActivityDetailResponse
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
    api_instance = plane.WorkItemActivityApi(api_client)
    issue_id = '550e8400-e29b-41d4-a716-446655440000' # str | Issue ID
    pk = '550e8400-e29b-41d4-a716-446655440000' # str | Activity ID
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    expand = 'assignees' # str | Comma-separated list of related fields to expand in response (optional)
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)
    order_by = '-created_at' # str | Field to order results by. Prefix with '-' for descending order (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # Endpoints for issue activity/search and fetch issue activity details
        api_response = api_instance.retrieve_work_item_activity(issue_id, pk, project_id, slug, cursor=cursor, expand=expand, fields=fields, order_by=order_by, per_page=per_page)
        print("The response of WorkItemActivityApi->retrieve_work_item_activity:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemActivityApi->retrieve_work_item_activity: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Activity ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **expand** | **str**| Comma-separated list of related fields to expand in response | [optional] 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 
 **order_by** | **str**| Field to order results by. Prefix with &#39;-&#39; for descending order | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedIssueActivityDetailResponse**](PaginatedIssueActivityDetailResponse.md)

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
**200** | Paginated list of work item activities |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

