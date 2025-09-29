# plane.EpicsApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**list_epics**](EpicsApi.md#list_epics) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/epics/ | List epics
[**retrieve_epic**](EpicsApi.md#retrieve_epic) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/epics/{pk}/ | Retrieve an epic


# **list_epics**
> PaginatedEpicResponse list_epics(project_id, slug, cursor=cursor, per_page=per_page)

List epics

List epics

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.paginated_epic_response import PaginatedEpicResponse
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
    api_instance = plane.EpicsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    cursor = '20:1:0' # str | Pagination cursor for getting next set of results (optional)
    per_page = 20 # int | Number of results per page (default: 20, max: 100) (optional)

    try:
        # List epics
        api_response = api_instance.list_epics(project_id, slug, cursor=cursor, per_page=per_page)
        print("The response of EpicsApi->list_epics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EpicsApi->list_epics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **cursor** | **str**| Pagination cursor for getting next set of results | [optional] 
 **per_page** | **int**| Number of results per page (default: 20, max: 100) | [optional] 

### Return type

[**PaginatedEpicResponse**](PaginatedEpicResponse.md)

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
**200** | Paginated list of epics |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_epic**
> Epic retrieve_epic(pk, project_id, slug, fields=fields)

Retrieve an epic

Retrieve an epic by id

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.epic import Epic
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
    api_instance = plane.EpicsApi(api_client)
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    fields = 'id,name,description' # str | Comma-separated list of fields to include in response (optional)

    try:
        # Retrieve an epic
        api_response = api_instance.retrieve_epic(pk, project_id, slug, fields=fields)
        print("The response of EpicsApi->retrieve_epic:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling EpicsApi->retrieve_epic: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pk** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **fields** | **str**| Comma-separated list of fields to include in response | [optional] 

### Return type

[**Epic**](Epic.md)

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
**200** | Epic |  -  |
**400** | Invalid request data provided |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

