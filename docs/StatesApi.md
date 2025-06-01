# plane.StatesApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_state**](StatesApi.md#create_state) | **POST** /workspaces/{slug}/projects/{project_id}/states/ | Create State
[**delete_state**](StatesApi.md#delete_state) | **DELETE** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Delete State
[**get_state**](StatesApi.md#get_state) | **GET** /workspaces/{slug}/projects/{project_id}/states/ | Get State
[**get_state2**](StatesApi.md#get_state2) | **GET** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Get State
[**update_state**](StatesApi.md#update_state) | **PATCH** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Update State


# **create_state**
> State create_state(project_id, slug, create_state_request=create_state_request)

Create State

Create a new state for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_state_request import CreateStateRequest
from plane.models.state import State
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
    api_instance = plane.StatesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    create_state_request = plane.CreateStateRequest() # CreateStateRequest |  (optional)

    try:
        # Create State
        api_response = api_instance.create_state(project_id, slug, create_state_request=create_state_request)
        print("The response of StatesApi->create_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StatesApi->create_state: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **create_state_request** | [**CreateStateRequest**](CreateStateRequest.md)|  | [optional] 

### Return type

[**State**](State.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | State created |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |
**409** | State with the same name already exists |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_state**
> delete_state(project_id, slug, state_id)

Delete State

Delete a state for a project

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
    api_instance = plane.StatesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 

    try:
        # Delete State
        api_instance.delete_state(project_id, slug, state_id)
    except Exception as e:
        print("Exception when calling StatesApi->delete_state: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state_id** | **str**|  | 

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
**204** | State deleted |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | State not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_state**
> State get_state(project_id, slug)

Get State

Get a state for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.state import State
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
    api_instance = plane.StatesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        # Get State
        api_response = api_instance.get_state(project_id, slug)
        print("The response of StatesApi->get_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StatesApi->get_state: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**State**](State.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | State retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_state2**
> State get_state2(project_id, slug, state_id)

Get State

Get a state for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.state import State
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
    api_instance = plane.StatesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 

    try:
        # Get State
        api_response = api_instance.get_state2(project_id, slug, state_id)
        print("The response of StatesApi->get_state2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StatesApi->get_state2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state_id** | **str**|  | 

### Return type

[**State**](State.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | State retrieved |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_state**
> State update_state(project_id, slug, state_id, create_state_request=create_state_request)

Update State

Update a state for a project

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_state_request import CreateStateRequest
from plane.models.state import State
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
    api_instance = plane.StatesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 
    create_state_request = plane.CreateStateRequest() # CreateStateRequest |  (optional)

    try:
        # Update State
        api_response = api_instance.update_state(project_id, slug, state_id, create_state_request=create_state_request)
        print("The response of StatesApi->update_state:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling StatesApi->update_state: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state_id** | **str**|  | 
 **create_state_request** | [**CreateStateRequest**](CreateStateRequest.md)|  | [optional] 

### Return type

[**State**](State.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | State updated |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | State not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

