# plane.WorkItemWorklogsApi

All URIs are relative to *https://api.plane.so*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_issue_worklog**](WorkItemWorklogsApi.md#create_issue_worklog) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/ | Create a new worklog entry
[**delete_issue_worklog**](WorkItemWorklogsApi.md#delete_issue_worklog) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/{pk}/ | Delete a worklog entry
[**get_project_worklog_summary**](WorkItemWorklogsApi.md#get_project_worklog_summary) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/total-worklogs/ | Get project worklog summary
[**list_issue_worklogs**](WorkItemWorklogsApi.md#list_issue_worklogs) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/ | List worklog entries
[**update_issue_worklog**](WorkItemWorklogsApi.md#update_issue_worklog) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/{pk}/ | Update a worklog entry


# **create_issue_worklog**
> IssueWorkLogAPI create_issue_worklog(issue_id, project_id, slug, issue_work_log_api_request=issue_work_log_api_request)

Create a new worklog entry

Create a new worklog entry

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_work_log_api import IssueWorkLogAPI
from plane.models.issue_work_log_api_request import IssueWorkLogAPIRequest
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
    api_instance = plane.WorkItemWorklogsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    issue_work_log_api_request = plane.IssueWorkLogAPIRequest() # IssueWorkLogAPIRequest |  (optional)

    try:
        # Create a new worklog entry
        api_response = api_instance.create_issue_worklog(issue_id, project_id, slug, issue_work_log_api_request=issue_work_log_api_request)
        print("The response of WorkItemWorklogsApi->create_issue_worklog:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemWorklogsApi->create_issue_worklog: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **issue_work_log_api_request** | [**IssueWorkLogAPIRequest**](IssueWorkLogAPIRequest.md)|  | [optional] 

### Return type

[**IssueWorkLogAPI**](IssueWorkLogAPI.md)

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
**404** | Worklog is not enabled for the project |  -  |
**201** | Worklog created successfully |  -  |
**400** | Invalid request data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_worklog**
> delete_issue_worklog(issue_id, pk, project_id, slug)

Delete a worklog entry

Delete a worklog entry

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
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
    api_instance = plane.WorkItemWorklogsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Delete a worklog entry
        api_instance.delete_issue_worklog(issue_id, pk, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkItemWorklogsApi->delete_issue_worklog: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
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
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Worklog not found or time tracking disabled |  -  |
**204** | Worklog deleted successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_project_worklog_summary**
> List[ProjectWorklogSummary] get_project_worklog_summary(project_id, slug)

Get project worklog summary

Get project worklog summary

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.project_worklog_summary import ProjectWorklogSummary
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
    api_instance = plane.WorkItemWorklogsApi(api_client)
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # Get project worklog summary
        api_response = api_instance.get_project_worklog_summary(project_id, slug)
        print("The response of WorkItemWorklogsApi->get_project_worklog_summary:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemWorklogsApi->get_project_worklog_summary: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[ProjectWorklogSummary]**](ProjectWorklogSummary.md)

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
**404** | Worklog is not enabled for the project |  -  |
**200** | Project worklog summary by issue |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_issue_worklogs**
> List[IssueWorkLogAPI] list_issue_worklogs(issue_id, project_id, slug)

List worklog entries

List worklog entries

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_work_log_api import IssueWorkLogAPI
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
    api_instance = plane.WorkItemWorklogsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug

    try:
        # List worklog entries
        api_response = api_instance.list_issue_worklogs(issue_id, project_id, slug)
        print("The response of WorkItemWorklogsApi->list_issue_worklogs:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemWorklogsApi->list_issue_worklogs: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**List[IssueWorkLogAPI]**](IssueWorkLogAPI.md)

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
**404** | Worklog is not enabled for the project |  -  |
**200** | List of worklog entries |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_worklog**
> IssueWorkLogAPI update_issue_worklog(issue_id, pk, project_id, slug, patched_issue_work_log_api_request=patched_issue_work_log_api_request)

Update a worklog entry

Update a worklog entry

### Example

* Api Key Authentication (ApiKeyAuthentication):
* OAuth Authentication (OAuth2Authentication):
* OAuth Authentication (OAuth2Authentication):
```python
import time
import os
import plane
from plane.models.issue_work_log_api import IssueWorkLogAPI
from plane.models.patched_issue_work_log_api_request import PatchedIssueWorkLogAPIRequest
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
    api_instance = plane.WorkItemWorklogsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    pk = 'pk_example' # str | 
    project_id = '550e8400-e29b-41d4-a716-446655440000' # str | Project ID
    slug = 'my-workspace' # str | Workspace slug
    patched_issue_work_log_api_request = plane.PatchedIssueWorkLogAPIRequest() # PatchedIssueWorkLogAPIRequest |  (optional)

    try:
        # Update a worklog entry
        api_response = api_instance.update_issue_worklog(issue_id, pk, project_id, slug, patched_issue_work_log_api_request=patched_issue_work_log_api_request)
        print("The response of WorkItemWorklogsApi->update_issue_worklog:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemWorklogsApi->update_issue_worklog: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **pk** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **patched_issue_work_log_api_request** | [**PatchedIssueWorkLogAPIRequest**](PatchedIssueWorkLogAPIRequest.md)|  | [optional] 

### Return type

[**IssueWorkLogAPI**](IssueWorkLogAPI.md)

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
**404** | Worklog not found or time tracking disabled |  -  |
**200** | Worklog updated successfully |  -  |
**400** | Invalid request data |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

