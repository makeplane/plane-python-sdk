# plane.GeneralApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**search_issues**](GeneralApi.md#search_issues) | **GET** /workspaces/{slug}/issues/search/ | Search issues
[**workspaces_issues_retrieve**](GeneralApi.md#workspaces_issues_retrieve) | **GET** /workspaces/{slug}/issues/{project__identifier}-{issue__identifier}/ | Retrieve Issues


# **search_issues**
> SearchIssues200Response search_issues(search, slug, limit=limit, project_id=project_id, workspace_search=workspace_search)

Search issues

Search issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.search_issues200_response import SearchIssues200Response
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
    api_instance = plane.GeneralApi(api_client)
    search = 'search_example' # str | Search query
    slug = 'slug_example' # str | Workspace slug
    limit = 56 # int | Limit (optional)
    project_id = 'project_id_example' # str | Project ID (optional)
    workspace_search = 'workspace_search_example' # str | Workspace search (optional)

    try:
        # Search issues
        api_response = api_instance.search_issues(search, slug, limit=limit, project_id=project_id, workspace_search=workspace_search)
        print("The response of GeneralApi->search_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeneralApi->search_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **search** | **str**| Search query | 
 **slug** | **str**| Workspace slug | 
 **limit** | **int**| Limit | [optional] 
 **project_id** | **str**| Project ID | [optional] 
 **workspace_search** | **str**| Workspace search | [optional] 

### Return type

[**SearchIssues200Response**](SearchIssues200Response.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issues |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_issues_retrieve**
> Issue workspaces_issues_retrieve(issue__identifier, project__identifier, slug)

Retrieve Issues

This viewset provides `retrieveByIssueId` on workspace level

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
    api_instance = plane.GeneralApi(api_client)
    issue__identifier = 'issue__identifier_example' # str | 
    project__identifier = 'project__identifier_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Retrieve Issues
        api_response = api_instance.workspaces_issues_retrieve(issue__identifier, project__identifier, slug)
        print("The response of GeneralApi->workspaces_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GeneralApi->workspaces_issues_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue__identifier** | **str**|  | 
 **project__identifier** | **str**|  | 
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
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

