# plane.IntakeApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_intake_issue**](IntakeApi.md#create_intake_issue) | **POST** /workspaces/{slug}/projects/{project_id}/intake-issues/ | Create intake issue
[**delete_intake_issue**](IntakeApi.md#delete_intake_issue) | **DELETE** /workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Delete intake issue
[**get_intake_issues**](IntakeApi.md#get_intake_issues) | **GET** /workspaces/{slug}/projects/{project_id}/intake-issues/ | Get intake issues
[**get_intake_issues2**](IntakeApi.md#get_intake_issues2) | **GET** /workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Get intake issues
[**update_intake_issue**](IntakeApi.md#update_intake_issue) | **PATCH** /workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Update intake issue


# **create_intake_issue**
> IntakeIssue create_intake_issue(project_id, slug, create_intake_issue_request=create_intake_issue_request)

Create intake issue

Create intake issue

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_intake_issue_request import CreateIntakeIssueRequest
from plane.models.intake_issue import IntakeIssue
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
    api_instance = plane.IntakeApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_intake_issue_request = plane.CreateIntakeIssueRequest() # CreateIntakeIssueRequest |  (optional)

    try:
        # Create intake issue
        api_response = api_instance.create_intake_issue(project_id, slug, create_intake_issue_request=create_intake_issue_request)
        print("The response of IntakeApi->create_intake_issue:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntakeApi->create_intake_issue: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_intake_issue_request** | [**CreateIntakeIssueRequest**](CreateIntakeIssueRequest.md)|  | [optional] 

### Return type

[**IntakeIssue**](IntakeIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Intake issue created |  -  |
**400** | Invalid request |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_intake_issue**
> delete_intake_issue(issue_id, project_id, slug)

Delete intake issue

Delete intake issue

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
    api_instance = plane.IntakeApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Delete intake issue
        api_instance.delete_intake_issue(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling IntakeApi->delete_intake_issue: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
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
**204** | Intake issue deleted |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Intake issue not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_intake_issues**
> IntakeIssue get_intake_issues(project_id, slug)

Get intake issues

Get intake issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.intake_issue import IntakeIssue
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
    api_instance = plane.IntakeApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get intake issues
        api_response = api_instance.get_intake_issues(project_id, slug)
        print("The response of IntakeApi->get_intake_issues:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntakeApi->get_intake_issues: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IntakeIssue**](IntakeIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Intake issues |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_intake_issues2**
> IntakeIssue get_intake_issues2(issue_id, project_id, slug)

Get intake issues

Get intake issues

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.intake_issue import IntakeIssue
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
    api_instance = plane.IntakeApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get intake issues
        api_response = api_instance.get_intake_issues2(issue_id, project_id, slug)
        print("The response of IntakeApi->get_intake_issues2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntakeApi->get_intake_issues2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IntakeIssue**](IntakeIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Intake issues |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_intake_issue**
> IntakeIssue update_intake_issue(issue_id, project_id, slug, create_intake_issue_request_issue=create_intake_issue_request_issue)

Update intake issue

Update intake issue

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_intake_issue_request_issue import CreateIntakeIssueRequestIssue
from plane.models.intake_issue import IntakeIssue
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
    api_instance = plane.IntakeApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_intake_issue_request_issue = plane.CreateIntakeIssueRequestIssue() # CreateIntakeIssueRequestIssue |  (optional)

    try:
        # Update intake issue
        api_response = api_instance.update_intake_issue(issue_id, project_id, slug, create_intake_issue_request_issue=create_intake_issue_request_issue)
        print("The response of IntakeApi->update_intake_issue:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling IntakeApi->update_intake_issue: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_intake_issue_request_issue** | [**CreateIntakeIssueRequestIssue**](CreateIntakeIssueRequestIssue.md)|  | [optional] 

### Return type

[**IntakeIssue**](IntakeIssue.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

