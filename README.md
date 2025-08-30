# plane-sdk
The Plane REST API

Visit our quick start guide and full API documentation at [developers.plane.so](https://developers.plane.so/api-reference/introduction).

- API version: 0.0.1
- Package version: 0.1.9
- Generator version: 7.13.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen
For more information, please visit [https://plane.so](https://plane.so)

## Requirements.

Python 3.9+

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install plane-sdk
```
(you may need to run `pip` with root permission: `sudo pip install plane-sdk`)

Then import the package:
```python
import plane
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import plane
```

### Tests

Execute `pytest` to run the tests.

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from plane.configuration import Configuration
from plane.api_client import ApiClient
from plane.api.users_api import UsersApi
from plane.api.projects_api import ProjectsApi
from plane.exceptions import ApiException

def test_api():

    # Configure API Key authentication
    configuration = Configuration(
        api_key={'ApiKeyAuthentication': <API_KEY>}
    )

    # Configure Access Token authentication
    # configuration = Configuration(
    #    access_token='<PLANE_ACCESS_TOKEN>'
    # )

    # Create API client instance
    api_client = ApiClient(configuration)

    # Create Users API instance
    users_api = UsersApi(api_client)

    # Call get_current_user endpoint
    print("Fetching current user information...")
    user = users_api.get_current_user()
    print(user.email)

    projects_api = ProjectsApi(api_client)
    projects_response = projects_api.list_projects(slug="<workspace_slug>")
    for project in projects_response.results:
        print(f"{project.id} - {project.name}")
```

## Documentation for API Endpoints

All URIs are relative to *https://api.plane.so*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*AssetsApi* | [**create_generic_asset_upload**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#create_generic_asset_upload) | **POST** /api/v1/workspaces/{slug}/assets/ | Generate presigned URL for generic asset upload
*AssetsApi* | [**create_user_asset_upload**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#create_user_asset_upload) | **POST** /api/v1/assets/user-assets/ | Generate presigned URL for user asset upload
*AssetsApi* | [**delete_user_asset**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#delete_user_asset) | **DELETE** /api/v1/assets/user-assets/{asset_id}/ | Delete user asset
*AssetsApi* | [**get_generic_asset**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#get_generic_asset) | **GET** /api/v1/workspaces/{slug}/assets/{asset_id}/ | Get presigned URL for asset download
*AssetsApi* | [**update_generic_asset**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#update_generic_asset) | **PATCH** /api/v1/workspaces/{slug}/assets/{asset_id}/ | Update generic asset after upload completion
*AssetsApi* | [**update_user_asset**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AssetsApi.md#update_user_asset) | **PATCH** /api/v1/assets/user-assets/{asset_id}/ | Mark user asset as uploaded
*CyclesApi* | [**add_cycle_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#add_cycle_work_items) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | Add Work Items to Cycle
*CyclesApi* | [**archive_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#archive_cycle) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/archive/ | Archive cycle
*CyclesApi* | [**create_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#create_cycle) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/ | Create cycle
*CyclesApi* | [**delete_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#delete_cycle) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{pk}/ | Delete cycle
*CyclesApi* | [**delete_cycle_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#delete_cycle_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | Delete cycle work item
*CyclesApi* | [**list_archived_cycles**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#list_archived_cycles) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/archived-cycles/ | List archived cycles
*CyclesApi* | [**list_cycle_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#list_cycle_work_items) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | List cycle work items
*CyclesApi* | [**list_cycles**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#list_cycles) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/ | List cycles
*CyclesApi* | [**retrieve_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#retrieve_cycle) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{pk}/ | Retrieve cycle
*CyclesApi* | [**retrieve_cycle_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#retrieve_cycle_work_item) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | Retrieve cycle work item
*CyclesApi* | [**transfer_cycle_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#transfer_cycle_work_items) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/transfer-issues/ | Transfer cycle work items
*CyclesApi* | [**unarchive_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#unarchive_cycle) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/archived-cycles/{pk}/unarchive/ | Unarchive cycle
*CyclesApi* | [**update_cycle**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CyclesApi.md#update_cycle) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/cycles/{pk}/ | Update cycle
*IntakeApi* | [**create_intake_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeApi.md#create_intake_work_item) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/intake-issues/ | Create intake work item
*IntakeApi* | [**delete_intake_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeApi.md#delete_intake_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Delete intake work item
*IntakeApi* | [**get_intake_work_items_list**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeApi.md#get_intake_work_items_list) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/intake-issues/ | List intake work items
*IntakeApi* | [**retrieve_intake_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeApi.md#retrieve_intake_work_item) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Retrieve intake work item
*IntakeApi* | [**update_intake_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeApi.md#update_intake_work_item) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/intake-issues/{issue_id}/ | Update intake work item
*LabelsApi* | [**create_label**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelsApi.md#create_label) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/labels/ | Endpoints for label create/update/delete and fetch label details
*LabelsApi* | [**delete_label**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelsApi.md#delete_label) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Delete a label
*LabelsApi* | [**get_labels**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelsApi.md#get_labels) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Endpoints for label create/update/delete and fetch label details
*LabelsApi* | [**list_labels**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelsApi.md#list_labels) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/labels/ | Endpoints for label create/update/delete and fetch label details
*LabelsApi* | [**update_label**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelsApi.md#update_label) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/labels/{pk}/ | Update a label
*MembersApi* | [**get_project_members**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/MembersApi.md#get_project_members) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/members/ | List project members
*MembersApi* | [**get_workspace_members**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/MembersApi.md#get_workspace_members) | **GET** /api/v1/workspaces/{slug}/members/ | List workspace members
*ModulesApi* | [**add_module_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#add_module_work_items) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | Add Work Items to Module
*ModulesApi* | [**archive_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#archive_module) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/archive/ | Archive module
*ModulesApi* | [**create_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#create_module) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/modules/ | Create module
*ModulesApi* | [**delete_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#delete_module) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Delete module
*ModulesApi* | [**delete_module_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#delete_module_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | Delete module work item
*ModulesApi* | [**list_archived_modules**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#list_archived_modules) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/archived-modules/ | List archived modules
*ModulesApi* | [**list_module_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#list_module_work_items) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | List module work items
*ModulesApi* | [**list_modules**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#list_modules) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/ | List modules
*ModulesApi* | [**retrieve_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#retrieve_module) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Retrieve module
*ModulesApi* | [**unarchive_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#unarchive_module) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/archived-modules/{pk}/unarchive/ | Unarchive module
*ModulesApi* | [**update_module**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModulesApi.md#update_module) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/modules/{pk}/ | Update module
*ProjectsApi* | [**archive_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#archive_project) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/archive/ | Archive project
*ProjectsApi* | [**create_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#create_project) | **POST** /api/v1/workspaces/{slug}/projects/ | Create project
*ProjectsApi* | [**delete_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#delete_project) | **DELETE** /api/v1/workspaces/{slug}/projects/{pk}/ | Delete project
*ProjectsApi* | [**list_projects**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#list_projects) | **GET** /api/v1/workspaces/{slug}/projects/ | List or retrieve projects
*ProjectsApi* | [**retrieve_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#retrieve_project) | **GET** /api/v1/workspaces/{slug}/projects/{pk}/ | Retrieve project
*ProjectsApi* | [**unarchive_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#unarchive_project) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/archive/ | Unarchive project
*ProjectsApi* | [**update_project**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectsApi.md#update_project) | **PATCH** /api/v1/workspaces/{slug}/projects/{pk}/ | Update project
*StatesApi* | [**create_state**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StatesApi.md#create_state) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/states/ | Create state
*StatesApi* | [**delete_state**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StatesApi.md#delete_state) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Delete state
*StatesApi* | [**list_states**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StatesApi.md#list_states) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/states/ | List states
*StatesApi* | [**retrieve_state**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StatesApi.md#retrieve_state) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Retrieve state
*StatesApi* | [**update_state**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StatesApi.md#update_state) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/states/{state_id}/ | Update state
*UsersApi* | [**get_current_user**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/UsersApi.md#get_current_user) | **GET** /api/v1/users/me/ | Get current user
*WorkItemActivityApi* | [**list_work_item_activities**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemActivityApi.md#list_work_item_activities) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/ | Endpoints for issue activity/search and fetch issue activity details
*WorkItemActivityApi* | [**retrieve_work_item_activity**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemActivityApi.md#retrieve_work_item_activity) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/{pk}/ | Endpoints for issue activity/search and fetch issue activity details
*WorkItemAttachmentsApi* | [**create_work_item_attachment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemAttachmentsApi.md#create_work_item_attachment) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | Endpoints for issue attachment create/update/delete and fetch issue attachment details
*WorkItemAttachmentsApi* | [**delete_work_item_attachment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemAttachmentsApi.md#delete_work_item_attachment) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/{pk}/ | Endpoints for issue attachment create/update/delete and fetch issue attachment details
*WorkItemAttachmentsApi* | [**list_work_item_attachments**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemAttachmentsApi.md#list_work_item_attachments) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | Endpoints for issue attachment create/update/delete and fetch issue attachment details
*WorkItemAttachmentsApi* | [**retrieve_work_item_attachment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemAttachmentsApi.md#retrieve_work_item_attachment) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/{pk}/ | Endpoints for issue attachment create/update/delete and fetch issue attachment details
*WorkItemCommentsApi* | [**create_work_item_comment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemCommentsApi.md#create_work_item_comment) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | Endpoints for issue comment create/update/delete and fetch issue comment details
*WorkItemCommentsApi* | [**delete_work_item_comment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemCommentsApi.md#delete_work_item_comment) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{pk}/ | Endpoints for issue comment create/update/delete and fetch issue comment details
*WorkItemCommentsApi* | [**list_work_item_comments**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemCommentsApi.md#list_work_item_comments) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | Endpoints for issue comment create/update/delete and fetch issue comment details
*WorkItemCommentsApi* | [**retrieve_work_item_comment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemCommentsApi.md#retrieve_work_item_comment) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{pk}/ | Endpoints for issue comment create/update/delete and fetch issue comment details
*WorkItemCommentsApi* | [**update_work_item_comment**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemCommentsApi.md#update_work_item_comment) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{pk}/ | Endpoints for issue comment create/update/delete and fetch issue comment details
*WorkItemLinksApi* | [**create_work_item_link**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemLinksApi.md#create_work_item_link) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Endpoints for issue link create/update/delete and fetch issue link details
*WorkItemLinksApi* | [**delete_work_item_link**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemLinksApi.md#delete_work_item_link) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Endpoints for issue link create/update/delete and fetch issue link details
*WorkItemLinksApi* | [**list_work_item_links**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemLinksApi.md#list_work_item_links) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | Endpoints for issue link create/update/delete and fetch issue link details
*WorkItemLinksApi* | [**retrieve_work_item_link**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemLinksApi.md#retrieve_work_item_link) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Endpoints for issue link create/update/delete and fetch issue link details
*WorkItemLinksApi* | [**update_issue_link**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemLinksApi.md#update_issue_link) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{pk}/ | Update an issue link
*WorkItemPropertiesApi* | [**create_issue_property**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#create_issue_property) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | Create a new issue property
*WorkItemPropertiesApi* | [**create_issue_property_option**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#create_issue_property_option) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | Create a new issue property option
*WorkItemPropertiesApi* | [**create_issue_property_value**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#create_issue_property_value) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | Create/update an issue property value
*WorkItemPropertiesApi* | [**delete_issue_property**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#delete_issue_property) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Delete an issue property
*WorkItemPropertiesApi* | [**delete_issue_property_option**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#delete_issue_property_option) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Delete an issue property option
*WorkItemPropertiesApi* | [**list_issue_properties**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#list_issue_properties) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | List issue properties
*WorkItemPropertiesApi* | [**list_issue_property_options**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#list_issue_property_options) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | List issue property options
*WorkItemPropertiesApi* | [**list_issue_property_values**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#list_issue_property_values) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | List issue property values
*WorkItemPropertiesApi* | [**retrieve_issue_property**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#retrieve_issue_property) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Get issue property by id
*WorkItemPropertiesApi* | [**retrieve_issue_property_option**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#retrieve_issue_property_option) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Get issue property option by id
*WorkItemPropertiesApi* | [**update_issue_property**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#update_issue_property) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | Update an issue property
*WorkItemPropertiesApi* | [**update_issue_property_option**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemPropertiesApi.md#update_issue_property_option) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | Update an issue property option
*WorkItemTypesApi* | [**create_issue_type**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemTypesApi.md#create_issue_type) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/ | Create a new issue type
*WorkItemTypesApi* | [**delete_issue_type**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemTypesApi.md#delete_issue_type) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Delete an issue type
*WorkItemTypesApi* | [**list_issue_types**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemTypesApi.md#list_issue_types) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/ | List issue types
*WorkItemTypesApi* | [**retrieve_issue_type**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemTypesApi.md#retrieve_issue_type) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Retrieve an issue type by id
*WorkItemTypesApi* | [**update_issue_type**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemTypesApi.md#update_issue_type) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | Update an issue type
*WorkItemWorklogsApi* | [**create_issue_worklog**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemWorklogsApi.md#create_issue_worklog) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/ | Create a new worklog entry
*WorkItemWorklogsApi* | [**delete_issue_worklog**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemWorklogsApi.md#delete_issue_worklog) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/{pk}/ | Delete a worklog entry
*WorkItemWorklogsApi* | [**get_project_worklog_summary**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemWorklogsApi.md#get_project_worklog_summary) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/total-worklogs/ | Get project worklog summary
*WorkItemWorklogsApi* | [**list_issue_worklogs**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemWorklogsApi.md#list_issue_worklogs) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/ | List worklog entries
*WorkItemWorklogsApi* | [**update_issue_worklog**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemWorklogsApi.md#update_issue_worklog) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{issue_id}/worklogs/{pk}/ | Update a worklog entry
*WorkItemsApi* | [**create_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#create_work_item) | **POST** /api/v1/workspaces/{slug}/projects/{project_id}/issues/ | Create work item
*WorkItemsApi* | [**delete_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#delete_work_item) | **DELETE** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Delete work item
*WorkItemsApi* | [**get_workspace_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#get_workspace_work_item) | **GET** /api/v1/workspaces/{slug}/issues/{project_identifier}-{issue_identifier}/ | Retrieve work item by identifiers
*WorkItemsApi* | [**list_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#list_work_items) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/ | List work items
*WorkItemsApi* | [**retrieve_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#retrieve_work_item) | **GET** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Retrieve work item
*WorkItemsApi* | [**search_work_items**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#search_work_items) | **GET** /api/v1/workspaces/{slug}/issues/search/ | 
*WorkItemsApi* | [**update_work_item**](https://github.com/makeplane/plane-python-sdk/blob/main/docs/WorkItemsApi.md#update_work_item) | **PATCH** /api/v1/workspaces/{slug}/projects/{project_id}/issues/{pk}/ | Partially update work item


## Documentation For Models

 - [AccessEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/AccessEnum.md)
 - [Cycle](https://github.com/makeplane/plane-python-sdk/blob/main/docs/Cycle.md)
 - [CycleCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CycleCreateRequest.md)
 - [CycleIssue](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CycleIssue.md)
 - [CycleIssueRequestRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CycleIssueRequestRequest.md)
 - [CycleLite](https://github.com/makeplane/plane-python-sdk/blob/main/docs/CycleLite.md)
 - [EntityTypeEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/EntityTypeEnum.md)
 - [GenericAssetUploadRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/GenericAssetUploadRequest.md)
 - [GetWorkspaceMembers200ResponseInner](https://github.com/makeplane/plane-python-sdk/blob/main/docs/GetWorkspaceMembers200ResponseInner.md)
 - [GroupEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/GroupEnum.md)
 - [IntakeIssue](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeIssue.md)
 - [IntakeIssueCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeIssueCreateRequest.md)
 - [IntakeWorkItemStatusEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IntakeWorkItemStatusEnum.md)
 - [Issue](https://github.com/makeplane/plane-python-sdk/blob/main/docs/Issue.md)
 - [IssueActivity](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueActivity.md)
 - [IssueAttachment](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueAttachment.md)
 - [IssueAttachmentUploadRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueAttachmentUploadRequest.md)
 - [IssueComment](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueComment.md)
 - [IssueCommentCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueCommentCreateRequest.md)
 - [IssueDetail](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueDetail.md)
 - [IssueExpand](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueExpand.md)
 - [IssueForIntakeRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueForIntakeRequest.md)
 - [IssueLink](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueLink.md)
 - [IssueLinkCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueLinkCreateRequest.md)
 - [IssuePropertyAPI](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyAPI.md)
 - [IssuePropertyAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyAPIRequest.md)
 - [IssuePropertyOptionAPI](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyOptionAPI.md)
 - [IssuePropertyOptionAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyOptionAPIRequest.md)
 - [IssuePropertyValueAPI](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyValueAPI.md)
 - [IssuePropertyValueAPIDetail](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyValueAPIDetail.md)
 - [IssuePropertyValueAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssuePropertyValueAPIRequest.md)
 - [IssueRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueRequest.md)
 - [IssueSearch](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueSearch.md)
 - [IssueSearchItem](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueSearchItem.md)
 - [IssueTypeAPI](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueTypeAPI.md)
 - [IssueTypeAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueTypeAPIRequest.md)
 - [IssueWorkLogAPI](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueWorkLogAPI.md)
 - [IssueWorkLogAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/IssueWorkLogAPIRequest.md)
 - [Label](https://github.com/makeplane/plane-python-sdk/blob/main/docs/Label.md)
 - [LabelCreateUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/LabelCreateUpdateRequest.md)
 - [Module](https://github.com/makeplane/plane-python-sdk/blob/main/docs/Module.md)
 - [ModuleCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModuleCreateRequest.md)
 - [ModuleIssue](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModuleIssue.md)
 - [ModuleIssueRequestRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModuleIssueRequestRequest.md)
 - [ModuleLite](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModuleLite.md)
 - [ModuleStatusEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ModuleStatusEnum.md)
 - [NetworkEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/NetworkEnum.md)
 - [PaginatedArchivedCycleResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedArchivedCycleResponse.md)
 - [PaginatedArchivedModuleResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedArchivedModuleResponse.md)
 - [PaginatedCycleIssueResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedCycleIssueResponse.md)
 - [PaginatedCycleResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedCycleResponse.md)
 - [PaginatedIntakeIssueResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIntakeIssueResponse.md)
 - [PaginatedIssueActivityDetailResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIssueActivityDetailResponse.md)
 - [PaginatedIssueActivityResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIssueActivityResponse.md)
 - [PaginatedIssueCommentResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIssueCommentResponse.md)
 - [PaginatedIssueLinkDetailResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIssueLinkDetailResponse.md)
 - [PaginatedIssueLinkResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedIssueLinkResponse.md)
 - [PaginatedLabelResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedLabelResponse.md)
 - [PaginatedModuleIssueResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedModuleIssueResponse.md)
 - [PaginatedModuleResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedModuleResponse.md)
 - [PaginatedProjectResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedProjectResponse.md)
 - [PaginatedStateResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedStateResponse.md)
 - [PaginatedWorkItemResponse](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PaginatedWorkItemResponse.md)
 - [PatchedAssetUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedAssetUpdateRequest.md)
 - [PatchedCycleUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedCycleUpdateRequest.md)
 - [PatchedGenericAssetUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedGenericAssetUpdateRequest.md)
 - [PatchedIntakeIssueUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIntakeIssueUpdateRequest.md)
 - [PatchedIssueCommentCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssueCommentCreateRequest.md)
 - [PatchedIssueLinkUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssueLinkUpdateRequest.md)
 - [PatchedIssuePropertyAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssuePropertyAPIRequest.md)
 - [PatchedIssuePropertyOptionAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssuePropertyOptionAPIRequest.md)
 - [PatchedIssueRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssueRequest.md)
 - [PatchedIssueTypeAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssueTypeAPIRequest.md)
 - [PatchedIssueWorkLogAPIRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedIssueWorkLogAPIRequest.md)
 - [PatchedLabelCreateUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedLabelCreateUpdateRequest.md)
 - [PatchedModuleUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedModuleUpdateRequest.md)
 - [PatchedProjectUpdateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedProjectUpdateRequest.md)
 - [PatchedStateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PatchedStateRequest.md)
 - [PriorityEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PriorityEnum.md)
 - [Project](https://github.com/makeplane/plane-python-sdk/blob/main/docs/Project.md)
 - [ProjectCreateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectCreateRequest.md)
 - [ProjectWorklogSummary](https://github.com/makeplane/plane-python-sdk/blob/main/docs/ProjectWorklogSummary.md)
 - [PropertyTypeEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/PropertyTypeEnum.md)
 - [RelationTypeEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/RelationTypeEnum.md)
 - [RetrieveWorkItemAttachment400Response](https://github.com/makeplane/plane-python-sdk/blob/main/docs/RetrieveWorkItemAttachment400Response.md)
 - [State](https://github.com/makeplane/plane-python-sdk/blob/main/docs/State.md)
 - [StateLite](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StateLite.md)
 - [StateRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/StateRequest.md)
 - [TimezoneEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/TimezoneEnum.md)
 - [TransferCycleIssueRequestRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/TransferCycleIssueRequestRequest.md)
 - [TransferCycleWorkItems200Response](https://github.com/makeplane/plane-python-sdk/blob/main/docs/TransferCycleWorkItems200Response.md)
 - [TransferCycleWorkItems400Response](https://github.com/makeplane/plane-python-sdk/blob/main/docs/TransferCycleWorkItems400Response.md)
 - [TypeEnum](https://github.com/makeplane/plane-python-sdk/blob/main/docs/TypeEnum.md)
 - [UserAssetUploadRequest](https://github.com/makeplane/plane-python-sdk/blob/main/docs/UserAssetUploadRequest.md)
 - [UserLite](https://github.com/makeplane/plane-python-sdk/blob/main/docs/UserLite.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="ApiKeyAuthentication"></a>
### ApiKeyAuthentication

- **Type**: API key
- **API key parameter name**: X-API-Key
- **Location**: HTTP header

<a id="OAuth2Authentication"></a>
### OAuth2Authentication

- **Type**: OAuth
- **Flow**: application
- **Authorization URL**: 
- **Scopes**: 
 - **read**: Read access to resources
 - **write**: Write access to resources

<a id="OAuth2Authentication"></a>
### OAuth2Authentication

- **Type**: OAuth
- **Flow**: accessCode
- **Authorization URL**: /auth/o/authorize-app/
- **Scopes**: 
 - **read**: Read access to resources
 - **write**: Write access to resources


## Author

support@plane.so


