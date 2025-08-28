# plane.MembersApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_project_members**](MembersApi.md#get_project_members) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/members/ | List project members
[**get_workspace_members**](MembersApi.md#get_workspace_members) | **GET** /api/v1/workspaces/{slug}/members/ | List workspace members


# **get_project_members**
> List[UserLite] get_project_members(project_id, slug)

List project members

Retrieve all users who are members of the specified project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.user_lite import UserLite
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
    api_instance = plane.MembersApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List project members
        api_response = api_instance.get_project_members(project_id, slug)
        print("The response of MembersApi->get_project_members:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MembersApi->get_project_members: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[UserLite]**](UserLite.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of project members with their roles |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_workspace_members**
> List[GetWorkspaceMembers200ResponseInner] get_workspace_members(slug)

List workspace members

Retrieve all users who are members of the specified workspace.

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):

```python
import plane
from plane.models.get_workspace_members200_response_inner import GetWorkspaceMembers200ResponseInner
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
    api_instance = plane.MembersApi(api_client)
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List workspace members
        api_response = api_instance.get_workspace_members(slug)
        print("The response of MembersApi->get_workspace_members:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MembersApi->get_workspace_members: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**| Workspace slug | 

### Return type

[**List[GetWorkspaceMembers200ResponseInner]**](GetWorkspaceMembers200ResponseInner.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication), [OAuth2Authentication](../README.md#OAuth2Authentication), [OAuth2Authentication](../README.md#OAuth2Authentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of workspace members with their roles |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

