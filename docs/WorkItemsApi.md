# plane.WorkItemsApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_issue_comment**](WorkItemsApi.md#create_issue_comment) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | Create an issue comment
[**create_issue_link**](WorkItemsApi.md#create_issue_link) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Create an issue link
[**create_work_item**](WorkItemsApi.md#create_work_item) | **POST** /workspaces/{slug}/projects/{project_id}/issues/ | Create an work item
[**delete_issue_attachment**](WorkItemsApi.md#delete_issue_attachment) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/{id}/ | Delete an issue attachment
[**delete_issue_comment**](WorkItemsApi.md#delete_issue_comment) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | Delete an issue comment
[**delete_issue_link**](WorkItemsApi.md#delete_issue_link) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | Delete an issue link
[**delete_work_item**](WorkItemsApi.md#delete_work_item) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | Delete an work item
[**get_issue_activities**](WorkItemsApi.md#get_issue_activities) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/ | Get issue activities
[**get_issue_activities2**](WorkItemsApi.md#get_issue_activities2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/{id}/ | Get issue activities
[**get_issue_attachment**](WorkItemsApi.md#get_issue_attachment) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | Get an issue attachment
[**get_issue_attachment2**](WorkItemsApi.md#get_issue_attachment2) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | Get issue attachment
[**get_issue_attachment3**](WorkItemsApi.md#get_issue_attachment3) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/{id}/ | Get an issue attachment
[**get_issue_comments**](WorkItemsApi.md#get_issue_comments) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | Get issue comments
[**get_issue_comments2**](WorkItemsApi.md#get_issue_comments2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | Get issue comments
[**get_issue_links**](WorkItemsApi.md#get_issue_links) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Get issue links
[**get_issue_links2**](WorkItemsApi.md#get_issue_links2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | Get issue links
[**get_work_item**](WorkItemsApi.md#get_work_item) | **GET** /workspaces/{slug}/projects/{project_id}/issues/ | Work Item retrieve endpoints
[**get_work_item2**](WorkItemsApi.md#get_work_item2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | Work Item retrieve endpoints
[**patch_work_item**](WorkItemsApi.md#patch_work_item) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | Patch an work item
[**update_issue_comment**](WorkItemsApi.md#update_issue_comment) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | Update an issue comment
[**update_issue_link**](WorkItemsApi.md#update_issue_link) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | Update an issue link


# **create_issue_comment**
> IssueComment create_issue_comment(issue_id, issue_id2, project_id, project_id2, slug, slug2, create_issue_comment_request=create_issue_comment_request)

Create an issue comment

Create a new comment for an issue.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_issue_comment_request import CreateIssueCommentRequest
from plane.models.issue_comment import IssueComment
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    create_issue_comment_request = plane.CreateIssueCommentRequest() # CreateIssueCommentRequest |  (optional)

    try:
        # Create an issue comment
        api_response = api_instance.create_issue_comment(issue_id, issue_id2, project_id, project_id2, slug, slug2, create_issue_comment_request=create_issue_comment_request)
        print("The response of WorkItemsApi->create_issue_comment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->create_issue_comment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **create_issue_comment_request** | [**CreateIssueCommentRequest**](CreateIssueCommentRequest.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Issue comment created successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_issue_link**
> IssueLink create_issue_link(issue_id, issue_id2, project_id, project_id2, slug, slug2, create_issue_link_request=create_issue_link_request)

Create an issue link

Create a new issue link in a project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_issue_link_request import CreateIssueLinkRequest
from plane.models.issue_link import IssueLink
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    create_issue_link_request = plane.CreateIssueLinkRequest() # CreateIssueLinkRequest |  (optional)

    try:
        # Create an issue link
        api_response = api_instance.create_issue_link(issue_id, issue_id2, project_id, project_id2, slug, slug2, create_issue_link_request=create_issue_link_request)
        print("The response of WorkItemsApi->create_issue_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->create_issue_link: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **create_issue_link_request** | [**CreateIssueLinkRequest**](CreateIssueLinkRequest.md)|  | [optional] 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Issue link created successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_work_item**
> Issue create_work_item(project_id, slug, issue)

Create an work item

Create a new work item in the project.

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
    api_instance = plane.WorkItemsApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue = plane.Issue() # Issue | 

    try:
        # Create an work item
        api_response = api_instance.create_work_item(project_id, slug, issue)
        print("The response of WorkItemsApi->create_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->create_work_item: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue** | [**Issue**](Issue.md)|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Work Item created successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_attachment**
> delete_issue_attachment(id, issue_id, pk, project_id, slug, slug2)

Delete an issue attachment

Delete an issue attachment

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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue Attachment ID
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Delete an issue attachment
        api_instance.delete_issue_attachment(id, issue_id, pk, project_id, slug, slug2)
    except Exception as e:
        print("Exception when calling WorkItemsApi->delete_issue_attachment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Issue Attachment ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

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
**204** | Issue attachment deleted successfully |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue attachment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_comment**
> delete_issue_comment(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2)

Delete an issue comment

Delete an existing comment for an issue.

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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue comment ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Delete an issue comment
        api_instance.delete_issue_comment(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2)
    except Exception as e:
        print("Exception when calling WorkItemsApi->delete_issue_comment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **pk** | **str**| Issue comment ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

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
**204** | Issue comment deleted successfully |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue comment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_issue_link**
> delete_issue_link(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2)

Delete an issue link

Delete an issue link in a project.

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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue link ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Delete an issue link
        api_instance.delete_issue_link(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2)
    except Exception as e:
        print("Exception when calling WorkItemsApi->delete_issue_link: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **pk** | **str**| Issue link ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

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
**204** | Issue link deleted successfully |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue link not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_work_item**
> delete_work_item(id, project_id, slug)

Delete an work item

Delete an existing work item in the project.

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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete an work item
        api_instance.delete_work_item(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkItemsApi->delete_work_item: %s\n" % e)
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
**204** | Work Item deleted successfully |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Work Item not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_activities**
> IssueActivity get_issue_activities(issue_id, project_id, slug)

Get issue activities

Get issue activities

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_activity import IssueActivity
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug

    try:
        # Get issue activities
        api_response = api_instance.get_issue_activities(issue_id, project_id, slug)
        print("The response of WorkItemsApi->get_issue_activities:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_activities: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**IssueActivity**](IssueActivity.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue activities |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_activities2**
> IssueActivity get_issue_activities2(id, issue_id, project_id, slug)

Get issue activities

Get issue activities

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_activity import IssueActivity
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug

    try:
        # Get issue activities
        api_response = api_instance.get_issue_activities2(id, issue_id, project_id, slug)
        print("The response of WorkItemsApi->get_issue_activities2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_activities2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**| Issue ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

### Return type

[**IssueActivity**](IssueActivity.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue activities |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_attachment**
> IssueAttachment get_issue_attachment(issue_id, project_id, slug, slug2)

Get an issue attachment

Get an issue attachment

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_attachment import IssueAttachment
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get an issue attachment
        api_response = api_instance.get_issue_attachment(issue_id, project_id, slug, slug2)
        print("The response of WorkItemsApi->get_issue_attachment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_attachment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueAttachment**](IssueAttachment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue attachment |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue attachment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_attachment2**
> get_issue_attachment2(issue_id, pk, project_id, slug, get_issue_attachment2_request=get_issue_attachment2_request)

Get issue attachment


        Get an issue attachment.
        

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.get_issue_attachment2_request import GetIssueAttachment2Request
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue Attachment ID
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug
    get_issue_attachment2_request = plane.GetIssueAttachment2Request() # GetIssueAttachment2Request |  (optional)

    try:
        # Get issue attachment
        api_instance.get_issue_attachment2(issue_id, pk, project_id, slug, get_issue_attachment2_request=get_issue_attachment2_request)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_attachment2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**| Issue ID | 
 **pk** | **str**| Issue Attachment ID | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 
 **get_issue_attachment2_request** | [**GetIssueAttachment2Request**](GetIssueAttachment2Request.md)|  | [optional] 

### Return type

void (empty response body)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Presigned download URL generated successfully |  -  |
**400** | Validation error |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue or Project or Workspace not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_attachment3**
> IssueAttachment get_issue_attachment3(id, issue_id, project_id, slug, slug2)

Get an issue attachment

Get an issue attachment

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_attachment import IssueAttachment
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get an issue attachment
        api_response = api_instance.get_issue_attachment3(id, issue_id, project_id, slug, slug2)
        print("The response of WorkItemsApi->get_issue_attachment3:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_attachment3: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueAttachment**](IssueAttachment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue attachment |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue attachment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_comments**
> IssueComment get_issue_comments(issue_id, issue_id2, project_id, project_id2, slug, slug2)

Get issue comments

Get all comments for an issue.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get issue comments
        api_response = api_instance.get_issue_comments(issue_id, issue_id2, project_id, project_id2, slug, slug2)
        print("The response of WorkItemsApi->get_issue_comments:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_comments: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue comments |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_comments2**
> IssueComment get_issue_comments2(id, issue_id, issue_id2, project_id, project_id2, slug, slug2)

Get issue comments

Get all comments for an issue.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get issue comments
        api_response = api_instance.get_issue_comments2(id, issue_id, issue_id2, project_id, project_id2, slug, slug2)
        print("The response of WorkItemsApi->get_issue_comments2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_comments2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue comments |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_links**
> IssueLink get_issue_links(issue_id, issue_id2, project_id, project_id2, slug, slug2)

Get issue links

Get all issue links in a project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
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
    api_instance = plane.WorkItemsApi(api_client)
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get issue links
        api_response = api_instance.get_issue_links(issue_id, issue_id2, project_id, project_id2, slug, slug2)
        print("The response of WorkItemsApi->get_issue_links:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_links: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue links |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_issue_links2**
> IssueLink get_issue_links2(id, issue_id, issue_id2, project_id, project_id2, slug, slug2)

Get issue links

Get all issue links in a project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get issue links
        api_response = api_instance.get_issue_links2(id, issue_id, issue_id2, project_id, project_id2, slug, slug2)
        print("The response of WorkItemsApi->get_issue_links2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_issue_links2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue links |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_item**
> Issue get_work_item(project_id, slug)

Work Item retrieve endpoints


        List all work items in a project if pk is None, otherwise retrieve a specific work item.

        When pk is None:
        Returns a list of all work items in the project.

        When pk is provided:
        Returns the details of a specific work item.
        

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
    api_instance = plane.WorkItemsApi(api_client)
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug

    try:
        # Work Item retrieve endpoints
        api_response = api_instance.get_work_item(project_id, slug)
        print("The response of WorkItemsApi->get_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_work_item: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

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
**200** | List of issues or issue details |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_work_item2**
> Issue get_work_item2(id, project_id, slug)

Work Item retrieve endpoints


        List all work items in a project if pk is None, otherwise retrieve a specific work item.

        When pk is None:
        Returns a list of all work items in the project.

        When pk is provided:
        Returns the details of a specific work item.
        

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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | Workspace slug

    try:
        # Work Item retrieve endpoints
        api_response = api_instance.get_work_item2(id, project_id, slug)
        print("The response of WorkItemsApi->get_work_item2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->get_work_item2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**| Project ID | 
 **slug** | **str**| Workspace slug | 

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
**200** | List of issues or issue details |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_work_item**
> Issue patch_work_item(id, project_id, slug, patched_issue=patched_issue)

Patch an work item

Patch an existing work item in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.models.patched_issue import PatchedIssue
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue = plane.PatchedIssue() # PatchedIssue |  (optional)

    try:
        # Patch an work item
        api_response = api_instance.patch_work_item(id, project_id, slug, patched_issue=patched_issue)
        print("The response of WorkItemsApi->patch_work_item:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->patch_work_item: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue** | [**PatchedIssue**](PatchedIssue.md)|  | [optional] 

### Return type

[**Issue**](Issue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Work Item patched successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Work Item not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_comment**
> IssueComment update_issue_comment(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2, create_issue_comment_request=create_issue_comment_request)

Update an issue comment

Update an existing comment for an issue.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_issue_comment_request import CreateIssueCommentRequest
from plane.models.issue_comment import IssueComment
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue comment ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    create_issue_comment_request = plane.CreateIssueCommentRequest() # CreateIssueCommentRequest |  (optional)

    try:
        # Update an issue comment
        api_response = api_instance.update_issue_comment(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2, create_issue_comment_request=create_issue_comment_request)
        print("The response of WorkItemsApi->update_issue_comment:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->update_issue_comment: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **pk** | **str**| Issue comment ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **create_issue_comment_request** | [**CreateIssueCommentRequest**](CreateIssueCommentRequest.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue comment updated successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue comment not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_issue_link**
> IssueLink update_issue_link(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2, create_issue_link_request=create_issue_link_request)

Update an issue link

Update an issue link in a project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_issue_link_request import CreateIssueLinkRequest
from plane.models.issue_link import IssueLink
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
    api_instance = plane.WorkItemsApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    issue_id2 = 'issue_id_example' # str | Issue ID
    pk = 'pk_example' # str | Issue link ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    create_issue_link_request = plane.CreateIssueLinkRequest() # CreateIssueLinkRequest |  (optional)

    try:
        # Update an issue link
        api_response = api_instance.update_issue_link(id, issue_id, issue_id2, pk, project_id, project_id2, slug, slug2, create_issue_link_request=create_issue_link_request)
        print("The response of WorkItemsApi->update_issue_link:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkItemsApi->update_issue_link: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **issue_id2** | **str**| Issue ID | 
 **pk** | **str**| Issue link ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **create_issue_link_request** | [**CreateIssueLinkRequest**](CreateIssueLinkRequest.md)|  | [optional] 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Issue link updated successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Issue link not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

