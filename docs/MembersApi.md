# plane.MembersApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_project_members**](MembersApi.md#get_project_members) | **GET** /workspaces/{slug}/projects/{project_id}/members/ | Get all the users that are present inside the project
[**get_workspace_members**](MembersApi.md#get_workspace_members) | **GET** /workspaces/{slug}/members/ | Get all the users that are present inside the workspace


# **get_project_members**
> UserLite get_project_members(project_id, slug)

Get all the users that are present inside the project

Get all the users that are present inside the project

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.user_lite import UserLite
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
    api_instance = plane.MembersApi(api_client)
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug

    try:
        # Get all the users that are present inside the project
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

[**UserLite**](UserLite.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

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

Get all the users that are present inside the workspace

Get all the users that are present inside the workspace

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.get_workspace_members200_response_inner import GetWorkspaceMembers200ResponseInner
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
    api_instance = plane.MembersApi(api_client)
    slug = 'slug_example' # str | Workspace slug

    try:
        # Get all the users that are present inside the workspace
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

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

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

