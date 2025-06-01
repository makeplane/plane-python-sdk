# plane.LabelsApi

All URIs are relative to */api/v1*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_label**](LabelsApi.md#create_label) | **POST** /workspaces/{slug}/projects/{project_id}/labels/ | Create a label
[**delete_label**](LabelsApi.md#delete_label) | **DELETE** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | Delete a label
[**get_labels**](LabelsApi.md#get_labels) | **GET** /workspaces/{slug}/projects/{project_id}/labels/ | Get labels
[**get_labels2**](LabelsApi.md#get_labels2) | **GET** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | Get labels
[**update_label**](LabelsApi.md#update_label) | **PATCH** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | Update a label


# **create_label**
> Label create_label(project_id, project_id2, slug, slug2, create_label_request=create_label_request)

Create a label

Create a new label in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.create_label_request import CreateLabelRequest
from plane.models.label import Label
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
    api_instance = plane.LabelsApi(api_client)
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    create_label_request = plane.CreateLabelRequest() # CreateLabelRequest |  (optional)

    try:
        # Create a label
        api_response = api_instance.create_label(project_id, project_id2, slug, slug2, create_label_request=create_label_request)
        print("The response of LabelsApi->create_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->create_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **create_label_request** | [**CreateLabelRequest**](CreateLabelRequest.md)|  | [optional] 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Label created successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_label**
> delete_label(id, pk, project_id, project_id2, slug, slug2)

Delete a label

Delete a label in the project.

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
    api_instance = plane.LabelsApi(api_client)
    id = 'id_example' # str | 
    pk = 'pk_example' # str | Label ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Delete a label
        api_instance.delete_label(id, pk, project_id, project_id2, slug, slug2)
    except Exception as e:
        print("Exception when calling LabelsApi->delete_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **pk** | **str**| Label ID | 
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
**204** | Label deleted successfully |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Label not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_labels**
> Label get_labels(project_id, project_id2, slug, slug2)

Get labels

Get all labels in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.label import Label
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
    api_instance = plane.LabelsApi(api_client)
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get labels
        api_response = api_instance.get_labels(project_id, project_id2, slug, slug2)
        print("The response of LabelsApi->get_labels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->get_labels: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Labels |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_labels2**
> Label get_labels2(id, project_id, project_id2, slug, slug2)

Get labels

Get all labels in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.label import Label
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
    api_instance = plane.LabelsApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug

    try:
        # Get labels
        api_response = api_instance.get_labels2(id, project_id, project_id2, slug, slug2)
        print("The response of LabelsApi->get_labels2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->get_labels2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Labels |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Project not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_label**
> Label update_label(id, pk, project_id, project_id2, slug, slug2, update_label_request=update_label_request)

Update a label

Update a label in the project.

### Example

* Api Key Authentication (ApiKeyAuthentication):
```python
import time
import os
import plane
from plane.models.label import Label
from plane.models.update_label_request import UpdateLabelRequest
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
    api_instance = plane.LabelsApi(api_client)
    id = 'id_example' # str | 
    pk = 'pk_example' # str | Label ID
    project_id = 'project_id_example' # str | 
    project_id2 = 'project_id_example' # str | Project ID
    slug = 'slug_example' # str | 
    slug2 = 'slug_example' # str | Workspace slug
    update_label_request = plane.UpdateLabelRequest() # UpdateLabelRequest |  (optional)

    try:
        # Update a label
        api_response = api_instance.update_label(id, pk, project_id, project_id2, slug, slug2, update_label_request=update_label_request)
        print("The response of LabelsApi->update_label:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling LabelsApi->update_label: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **pk** | **str**| Label ID | 
 **project_id** | **str**|  | 
 **project_id2** | **str**| Project ID | 
 **slug** | **str**|  | 
 **slug2** | **str**| Workspace slug | 
 **update_label_request** | [**UpdateLabelRequest**](UpdateLabelRequest.md)|  | [optional] 

### Return type

[**Label**](Label.md)

### Authorization

[ApiKeyAuthentication](../README.md#ApiKeyAuthentication)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Label updated successfully |  -  |
**400** | Invalid request data |  -  |
**401** | Authentication credentials were not provided or are invalid. |  -  |
**403** | Permission denied. User lacks required permissions. |  -  |
**404** | Label not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

