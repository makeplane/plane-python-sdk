# plane.WorkspacesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**workspaces_issues_retrieve**](WorkspacesApi.md#workspaces_issues_retrieve) | **GET** /workspaces/{slug}/issues/{project__identifier}-{issue__identifier}/ | 
[**workspaces_projects_archive_create**](WorkspacesApi.md#workspaces_projects_archive_create) | **POST** /workspaces/{slug}/projects/{project_id}/archive/ | 
[**workspaces_projects_archive_destroy**](WorkspacesApi.md#workspaces_projects_archive_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/archive/ | 
[**workspaces_projects_archived_cycles_create**](WorkspacesApi.md#workspaces_projects_archived_cycles_create) | **POST** /workspaces/{slug}/projects/{project_id}/archived-cycles/ | 
[**workspaces_projects_archived_cycles_destroy**](WorkspacesApi.md#workspaces_projects_archived_cycles_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/archived-cycles/ | 
[**workspaces_projects_archived_cycles_retrieve**](WorkspacesApi.md#workspaces_projects_archived_cycles_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/archived-cycles/ | 
[**workspaces_projects_archived_modules_create**](WorkspacesApi.md#workspaces_projects_archived_modules_create) | **POST** /workspaces/{slug}/projects/{project_id}/archived-modules/ | 
[**workspaces_projects_archived_modules_destroy**](WorkspacesApi.md#workspaces_projects_archived_modules_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/archived-modules/ | 
[**workspaces_projects_archived_modules_retrieve**](WorkspacesApi.md#workspaces_projects_archived_modules_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/archived-modules/ | 
[**workspaces_projects_create**](WorkspacesApi.md#workspaces_projects_create) | **POST** /workspaces/{slug}/projects/ | 
[**workspaces_projects_create2**](WorkspacesApi.md#workspaces_projects_create2) | **POST** /workspaces/{slug}/projects/{id}/ | 
[**workspaces_projects_cycles_archive_create**](WorkspacesApi.md#workspaces_projects_cycles_archive_create) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/archive/ | 
[**workspaces_projects_cycles_archive_destroy**](WorkspacesApi.md#workspaces_projects_cycles_archive_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/archive/ | 
[**workspaces_projects_cycles_archive_retrieve**](WorkspacesApi.md#workspaces_projects_cycles_archive_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/archive/ | 
[**workspaces_projects_cycles_create**](WorkspacesApi.md#workspaces_projects_cycles_create) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/ | 
[**workspaces_projects_cycles_create2**](WorkspacesApi.md#workspaces_projects_cycles_create2) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | 
[**workspaces_projects_cycles_cycle_issues_create**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_create) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | 
[**workspaces_projects_cycles_cycle_issues_create2**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_create2) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | 
[**workspaces_projects_cycles_cycle_issues_destroy**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | 
[**workspaces_projects_cycles_cycle_issues_destroy2**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | 
[**workspaces_projects_cycles_cycle_issues_retrieve**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/ | 
[**workspaces_projects_cycles_cycle_issues_retrieve2**](WorkspacesApi.md#workspaces_projects_cycles_cycle_issues_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{issue_id}/ | 
[**workspaces_projects_cycles_destroy**](WorkspacesApi.md#workspaces_projects_cycles_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/ | 
[**workspaces_projects_cycles_destroy2**](WorkspacesApi.md#workspaces_projects_cycles_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | 
[**workspaces_projects_cycles_partial_update**](WorkspacesApi.md#workspaces_projects_cycles_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/cycles/ | 
[**workspaces_projects_cycles_partial_update2**](WorkspacesApi.md#workspaces_projects_cycles_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | 
[**workspaces_projects_cycles_retrieve**](WorkspacesApi.md#workspaces_projects_cycles_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/ | 
[**workspaces_projects_cycles_retrieve2**](WorkspacesApi.md#workspaces_projects_cycles_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/cycles/{id}/ | 
[**workspaces_projects_cycles_transfer_issues_create**](WorkspacesApi.md#workspaces_projects_cycles_transfer_issues_create) | **POST** /workspaces/{slug}/projects/{project_id}/cycles/{cycle_id}/transfer-issues/ | 
[**workspaces_projects_destroy**](WorkspacesApi.md#workspaces_projects_destroy) | **DELETE** /workspaces/{slug}/projects/ | 
[**workspaces_projects_destroy2**](WorkspacesApi.md#workspaces_projects_destroy2) | **DELETE** /workspaces/{slug}/projects/{id}/ | 
[**workspaces_projects_inbox_issues_create**](WorkspacesApi.md#workspaces_projects_inbox_issues_create) | **POST** /workspaces/{slug}/projects/{project_id}/inbox-issues/ | 
[**workspaces_projects_inbox_issues_create2**](WorkspacesApi.md#workspaces_projects_inbox_issues_create2) | **POST** /workspaces/{slug}/projects/{project_id}/inbox-issues/{issue_id}/ | 
[**workspaces_projects_inbox_issues_destroy**](WorkspacesApi.md#workspaces_projects_inbox_issues_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/inbox-issues/ | 
[**workspaces_projects_inbox_issues_destroy2**](WorkspacesApi.md#workspaces_projects_inbox_issues_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/inbox-issues/{issue_id}/ | 
[**workspaces_projects_inbox_issues_partial_update**](WorkspacesApi.md#workspaces_projects_inbox_issues_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/inbox-issues/ | 
[**workspaces_projects_inbox_issues_partial_update2**](WorkspacesApi.md#workspaces_projects_inbox_issues_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/inbox-issues/{issue_id}/ | 
[**workspaces_projects_inbox_issues_retrieve**](WorkspacesApi.md#workspaces_projects_inbox_issues_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/inbox-issues/ | 
[**workspaces_projects_inbox_issues_retrieve2**](WorkspacesApi.md#workspaces_projects_inbox_issues_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/inbox-issues/{issue_id}/ | 
[**workspaces_projects_issue_properties_options_create**](WorkspacesApi.md#workspaces_projects_issue_properties_options_create) | **POST** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | 
[**workspaces_projects_issue_properties_options_create2**](WorkspacesApi.md#workspaces_projects_issue_properties_options_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | 
[**workspaces_projects_issue_properties_options_destroy**](WorkspacesApi.md#workspaces_projects_issue_properties_options_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | 
[**workspaces_projects_issue_properties_options_destroy2**](WorkspacesApi.md#workspaces_projects_issue_properties_options_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | 
[**workspaces_projects_issue_properties_options_partial_update**](WorkspacesApi.md#workspaces_projects_issue_properties_options_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | 
[**workspaces_projects_issue_properties_options_partial_update2**](WorkspacesApi.md#workspaces_projects_issue_properties_options_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | 
[**workspaces_projects_issue_properties_options_retrieve**](WorkspacesApi.md#workspaces_projects_issue_properties_options_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/ | 
[**workspaces_projects_issue_properties_options_retrieve2**](WorkspacesApi.md#workspaces_projects_issue_properties_options_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issue-properties/{property_id}/options/{option_id}/ | 
[**workspaces_projects_issue_types_create**](WorkspacesApi.md#workspaces_projects_issue_types_create) | **POST** /workspaces/{slug}/projects/{project_id}/issue-types/ | 
[**workspaces_projects_issue_types_create2**](WorkspacesApi.md#workspaces_projects_issue_types_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | 
[**workspaces_projects_issue_types_destroy**](WorkspacesApi.md#workspaces_projects_issue_types_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-types/ | 
[**workspaces_projects_issue_types_destroy2**](WorkspacesApi.md#workspaces_projects_issue_types_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | 
[**workspaces_projects_issue_types_issue_properties_create**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_create) | **POST** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | 
[**workspaces_projects_issue_types_issue_properties_create2**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | 
[**workspaces_projects_issue_types_issue_properties_destroy**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | 
[**workspaces_projects_issue_types_issue_properties_destroy2**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | 
[**workspaces_projects_issue_types_issue_properties_partial_update**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | 
[**workspaces_projects_issue_types_issue_properties_partial_update2**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | 
[**workspaces_projects_issue_types_issue_properties_retrieve**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/ | 
[**workspaces_projects_issue_types_issue_properties_retrieve2**](WorkspacesApi.md#workspaces_projects_issue_types_issue_properties_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/issue-properties/{property_id}/ | 
[**workspaces_projects_issue_types_partial_update**](WorkspacesApi.md#workspaces_projects_issue_types_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-types/ | 
[**workspaces_projects_issue_types_partial_update2**](WorkspacesApi.md#workspaces_projects_issue_types_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | 
[**workspaces_projects_issue_types_retrieve**](WorkspacesApi.md#workspaces_projects_issue_types_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issue-types/ | 
[**workspaces_projects_issue_types_retrieve2**](WorkspacesApi.md#workspaces_projects_issue_types_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issue-types/{type_id}/ | 
[**workspaces_projects_issues_activities_retrieve**](WorkspacesApi.md#workspaces_projects_issues_activities_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/ | 
[**workspaces_projects_issues_activities_retrieve2**](WorkspacesApi.md#workspaces_projects_issues_activities_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/activities/{id}/ | 
[**workspaces_projects_issues_comments_create**](WorkspacesApi.md#workspaces_projects_issues_comments_create) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | 
[**workspaces_projects_issues_comments_create2**](WorkspacesApi.md#workspaces_projects_issues_comments_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | 
[**workspaces_projects_issues_comments_destroy**](WorkspacesApi.md#workspaces_projects_issues_comments_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | 
[**workspaces_projects_issues_comments_destroy2**](WorkspacesApi.md#workspaces_projects_issues_comments_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | 
[**workspaces_projects_issues_comments_partial_update**](WorkspacesApi.md#workspaces_projects_issues_comments_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | 
[**workspaces_projects_issues_comments_partial_update2**](WorkspacesApi.md#workspaces_projects_issues_comments_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | 
[**workspaces_projects_issues_comments_retrieve**](WorkspacesApi.md#workspaces_projects_issues_comments_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/ | 
[**workspaces_projects_issues_comments_retrieve2**](WorkspacesApi.md#workspaces_projects_issues_comments_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/comments/{id}/ | 
[**workspaces_projects_issues_create**](WorkspacesApi.md#workspaces_projects_issues_create) | **POST** /workspaces/{slug}/projects/{project_id}/issues/ | 
[**workspaces_projects_issues_create2**](WorkspacesApi.md#workspaces_projects_issues_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | 
[**workspaces_projects_issues_destroy**](WorkspacesApi.md#workspaces_projects_issues_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/ | 
[**workspaces_projects_issues_destroy2**](WorkspacesApi.md#workspaces_projects_issues_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | 
[**workspaces_projects_issues_issue_attachments_create**](WorkspacesApi.md#workspaces_projects_issues_issue_attachments_create) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | 
[**workspaces_projects_issues_issue_attachments_destroy**](WorkspacesApi.md#workspaces_projects_issues_issue_attachments_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | 
[**workspaces_projects_issues_issue_attachments_retrieve**](WorkspacesApi.md#workspaces_projects_issues_issue_attachments_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-attachments/ | 
[**workspaces_projects_issues_issue_properties_values_create**](WorkspacesApi.md#workspaces_projects_issues_issue_properties_values_create) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | 
[**workspaces_projects_issues_issue_properties_values_retrieve**](WorkspacesApi.md#workspaces_projects_issues_issue_properties_values_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/issue-properties/{property_id}/values/ | 
[**workspaces_projects_issues_links_create**](WorkspacesApi.md#workspaces_projects_issues_links_create) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | 
[**workspaces_projects_issues_links_create2**](WorkspacesApi.md#workspaces_projects_issues_links_create2) | **POST** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | 
[**workspaces_projects_issues_links_destroy**](WorkspacesApi.md#workspaces_projects_issues_links_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | 
[**workspaces_projects_issues_links_destroy2**](WorkspacesApi.md#workspaces_projects_issues_links_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | 
[**workspaces_projects_issues_links_partial_update**](WorkspacesApi.md#workspaces_projects_issues_links_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | 
[**workspaces_projects_issues_links_partial_update2**](WorkspacesApi.md#workspaces_projects_issues_links_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | 
[**workspaces_projects_issues_links_retrieve**](WorkspacesApi.md#workspaces_projects_issues_links_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/ | 
[**workspaces_projects_issues_links_retrieve2**](WorkspacesApi.md#workspaces_projects_issues_links_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{issue_id}/links/{id}/ | 
[**workspaces_projects_issues_partial_update**](WorkspacesApi.md#workspaces_projects_issues_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/ | 
[**workspaces_projects_issues_partial_update2**](WorkspacesApi.md#workspaces_projects_issues_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | 
[**workspaces_projects_issues_retrieve**](WorkspacesApi.md#workspaces_projects_issues_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/issues/ | 
[**workspaces_projects_issues_retrieve2**](WorkspacesApi.md#workspaces_projects_issues_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | 
[**workspaces_projects_issues_update**](WorkspacesApi.md#workspaces_projects_issues_update) | **PUT** /workspaces/{slug}/projects/{project_id}/issues/ | 
[**workspaces_projects_issues_update2**](WorkspacesApi.md#workspaces_projects_issues_update2) | **PUT** /workspaces/{slug}/projects/{project_id}/issues/{id}/ | 
[**workspaces_projects_labels_create**](WorkspacesApi.md#workspaces_projects_labels_create) | **POST** /workspaces/{slug}/projects/{project_id}/labels/ | 
[**workspaces_projects_labels_create2**](WorkspacesApi.md#workspaces_projects_labels_create2) | **POST** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | 
[**workspaces_projects_labels_destroy**](WorkspacesApi.md#workspaces_projects_labels_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/labels/ | 
[**workspaces_projects_labels_destroy2**](WorkspacesApi.md#workspaces_projects_labels_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | 
[**workspaces_projects_labels_partial_update**](WorkspacesApi.md#workspaces_projects_labels_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/labels/ | 
[**workspaces_projects_labels_partial_update2**](WorkspacesApi.md#workspaces_projects_labels_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | 
[**workspaces_projects_labels_retrieve**](WorkspacesApi.md#workspaces_projects_labels_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/labels/ | 
[**workspaces_projects_labels_retrieve2**](WorkspacesApi.md#workspaces_projects_labels_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/labels/{id}/ | 
[**workspaces_projects_members_create**](WorkspacesApi.md#workspaces_projects_members_create) | **POST** /workspaces/{slug}/projects/{project_id}/members/ | 
[**workspaces_projects_members_retrieve**](WorkspacesApi.md#workspaces_projects_members_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/members/ | 
[**workspaces_projects_modules_archive_create**](WorkspacesApi.md#workspaces_projects_modules_archive_create) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{id}/archive/ | 
[**workspaces_projects_modules_archive_destroy**](WorkspacesApi.md#workspaces_projects_modules_archive_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{id}/archive/ | 
[**workspaces_projects_modules_archive_retrieve**](WorkspacesApi.md#workspaces_projects_modules_archive_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{id}/archive/ | 
[**workspaces_projects_modules_create**](WorkspacesApi.md#workspaces_projects_modules_create) | **POST** /workspaces/{slug}/projects/{project_id}/modules/ | 
[**workspaces_projects_modules_create2**](WorkspacesApi.md#workspaces_projects_modules_create2) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | 
[**workspaces_projects_modules_destroy**](WorkspacesApi.md#workspaces_projects_modules_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/ | 
[**workspaces_projects_modules_destroy2**](WorkspacesApi.md#workspaces_projects_modules_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | 
[**workspaces_projects_modules_module_issues_create**](WorkspacesApi.md#workspaces_projects_modules_module_issues_create) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | 
[**workspaces_projects_modules_module_issues_create2**](WorkspacesApi.md#workspaces_projects_modules_module_issues_create2) | **POST** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | 
[**workspaces_projects_modules_module_issues_destroy**](WorkspacesApi.md#workspaces_projects_modules_module_issues_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | 
[**workspaces_projects_modules_module_issues_destroy2**](WorkspacesApi.md#workspaces_projects_modules_module_issues_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | 
[**workspaces_projects_modules_module_issues_retrieve**](WorkspacesApi.md#workspaces_projects_modules_module_issues_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/ | 
[**workspaces_projects_modules_module_issues_retrieve2**](WorkspacesApi.md#workspaces_projects_modules_module_issues_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{module_id}/module-issues/{issue_id}/ | 
[**workspaces_projects_modules_partial_update**](WorkspacesApi.md#workspaces_projects_modules_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/modules/ | 
[**workspaces_projects_modules_partial_update2**](WorkspacesApi.md#workspaces_projects_modules_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | 
[**workspaces_projects_modules_retrieve**](WorkspacesApi.md#workspaces_projects_modules_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/modules/ | 
[**workspaces_projects_modules_retrieve2**](WorkspacesApi.md#workspaces_projects_modules_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/modules/{id}/ | 
[**workspaces_projects_partial_update**](WorkspacesApi.md#workspaces_projects_partial_update) | **PATCH** /workspaces/{slug}/projects/ | 
[**workspaces_projects_partial_update2**](WorkspacesApi.md#workspaces_projects_partial_update2) | **PATCH** /workspaces/{slug}/projects/{id}/ | 
[**workspaces_projects_retrieve**](WorkspacesApi.md#workspaces_projects_retrieve) | **GET** /workspaces/{slug}/projects/ | 
[**workspaces_projects_retrieve2**](WorkspacesApi.md#workspaces_projects_retrieve2) | **GET** /workspaces/{slug}/projects/{id}/ | 
[**workspaces_projects_states_create**](WorkspacesApi.md#workspaces_projects_states_create) | **POST** /workspaces/{slug}/projects/{project_id}/states/ | 
[**workspaces_projects_states_create2**](WorkspacesApi.md#workspaces_projects_states_create2) | **POST** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | 
[**workspaces_projects_states_destroy**](WorkspacesApi.md#workspaces_projects_states_destroy) | **DELETE** /workspaces/{slug}/projects/{project_id}/states/ | 
[**workspaces_projects_states_destroy2**](WorkspacesApi.md#workspaces_projects_states_destroy2) | **DELETE** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | 
[**workspaces_projects_states_partial_update**](WorkspacesApi.md#workspaces_projects_states_partial_update) | **PATCH** /workspaces/{slug}/projects/{project_id}/states/ | 
[**workspaces_projects_states_partial_update2**](WorkspacesApi.md#workspaces_projects_states_partial_update2) | **PATCH** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | 
[**workspaces_projects_states_retrieve**](WorkspacesApi.md#workspaces_projects_states_retrieve) | **GET** /workspaces/{slug}/projects/{project_id}/states/ | 
[**workspaces_projects_states_retrieve2**](WorkspacesApi.md#workspaces_projects_states_retrieve2) | **GET** /workspaces/{slug}/projects/{project_id}/states/{state_id}/ | 


# **workspaces_issues_retrieve**
> Issue workspaces_issues_retrieve(issue__identifier, project__identifier, slug)



This viewset provides `retrieveByIssueId` on workspace level

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue__identifier = 'issue__identifier_example' # str | 
    project__identifier = 'project__identifier_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_issues_retrieve(issue__identifier, project__identifier, slug)
        print("The response of WorkspacesApi->workspaces_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_issues_retrieve: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archive_create**
> workspaces_projects_archive_create(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archive_create(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archive_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archive_destroy**
> workspaces_projects_archive_destroy(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archive_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archive_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_cycles_create**
> workspaces_projects_archived_cycles_create(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_cycles_create(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_cycles_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_cycles_destroy**
> workspaces_projects_archived_cycles_destroy(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_cycles_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_cycles_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_cycles_retrieve**
> workspaces_projects_archived_cycles_retrieve(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_cycles_retrieve(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_cycles_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_modules_create**
> workspaces_projects_archived_modules_create(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_modules_create(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_modules_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_modules_destroy**
> workspaces_projects_archived_modules_destroy(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_modules_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_modules_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_archived_modules_retrieve**
> workspaces_projects_archived_modules_retrieve(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_archived_modules_retrieve(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_archived_modules_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_create**
> Project workspaces_projects_create(slug, project)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    slug = 'slug_example' # str | 
    project = plane.Project() # Project | 

    try:
        api_response = api_instance.workspaces_projects_create(slug, project)
        print("The response of WorkspacesApi->workspaces_projects_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**|  | 
 **project** | [**Project**](Project.md)|  | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_create2**
> Project workspaces_projects_create2(id, slug, project)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    slug = 'slug_example' # str | 
    project = plane.Project() # Project | 

    try:
        api_response = api_instance.workspaces_projects_create2(id, slug, project)
        print("The response of WorkspacesApi->workspaces_projects_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **slug** | **str**|  | 
 **project** | [**Project**](Project.md)|  | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_archive_create**
> workspaces_projects_cycles_archive_create(cycle_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_archive_create(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_archive_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_archive_destroy**
> workspaces_projects_cycles_archive_destroy(cycle_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_archive_destroy(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_archive_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_archive_retrieve**
> workspaces_projects_cycles_archive_retrieve(cycle_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_archive_retrieve(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_archive_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_create**
> Cycle workspaces_projects_cycles_create(project_id, slug, cycle)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    cycle = plane.Cycle() # Cycle | 

    try:
        api_response = api_instance.workspaces_projects_cycles_create(project_id, slug, cycle)
        print("The response of WorkspacesApi->workspaces_projects_cycles_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **cycle** | [**Cycle**](Cycle.md)|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_create2**
> Cycle workspaces_projects_cycles_create2(id, project_id, slug, cycle)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    cycle = plane.Cycle() # Cycle | 

    try:
        api_response = api_instance.workspaces_projects_cycles_create2(id, project_id, slug, cycle)
        print("The response of WorkspacesApi->workspaces_projects_cycles_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **cycle** | [**Cycle**](Cycle.md)|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_create**
> CycleIssue workspaces_projects_cycles_cycle_issues_create(cycle_id, project_id, slug, cycle_issue)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    cycle_issue = plane.CycleIssue() # CycleIssue | 

    try:
        api_response = api_instance.workspaces_projects_cycles_cycle_issues_create(cycle_id, project_id, slug, cycle_issue)
        print("The response of WorkspacesApi->workspaces_projects_cycles_cycle_issues_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **cycle_issue** | [**CycleIssue**](CycleIssue.md)|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_create2**
> CycleIssue workspaces_projects_cycles_cycle_issues_create2(cycle_id, issue_id, project_id, slug, cycle_issue)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    cycle_issue = plane.CycleIssue() # CycleIssue | 

    try:
        api_response = api_instance.workspaces_projects_cycles_cycle_issues_create2(cycle_id, issue_id, project_id, slug, cycle_issue)
        print("The response of WorkspacesApi->workspaces_projects_cycles_cycle_issues_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **cycle_issue** | [**CycleIssue**](CycleIssue.md)|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_destroy**
> workspaces_projects_cycles_cycle_issues_destroy(cycle_id, project_id, slug)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_cycle_issues_destroy(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_destroy2**
> workspaces_projects_cycles_cycle_issues_destroy2(cycle_id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_cycle_issues_destroy2(cycle_id, issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_retrieve**
> CycleIssue workspaces_projects_cycles_cycle_issues_retrieve(cycle_id, project_id, slug)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_cycles_cycle_issues_retrieve(cycle_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_cycles_cycle_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_cycle_issues_retrieve2**
> CycleIssue workspaces_projects_cycles_cycle_issues_retrieve2(cycle_id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`,
and `destroy` actions related to cycle issues.

### Example

```python
import time
import os
import plane
from plane.models.cycle_issue import CycleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_cycles_cycle_issues_retrieve2(cycle_id, issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_cycles_cycle_issues_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_cycle_issues_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**CycleIssue**](CycleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_destroy**
> workspaces_projects_cycles_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_destroy2**
> workspaces_projects_cycles_destroy2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_destroy2(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_partial_update**
> Cycle workspaces_projects_cycles_partial_update(project_id, slug, patched_cycle=patched_cycle)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.models.patched_cycle import PatchedCycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_cycle = plane.PatchedCycle() # PatchedCycle |  (optional)

    try:
        api_response = api_instance.workspaces_projects_cycles_partial_update(project_id, slug, patched_cycle=patched_cycle)
        print("The response of WorkspacesApi->workspaces_projects_cycles_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_cycle** | [**PatchedCycle**](PatchedCycle.md)|  | [optional] 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_partial_update2**
> Cycle workspaces_projects_cycles_partial_update2(id, project_id, slug, patched_cycle=patched_cycle)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.models.patched_cycle import PatchedCycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_cycle = plane.PatchedCycle() # PatchedCycle |  (optional)

    try:
        api_response = api_instance.workspaces_projects_cycles_partial_update2(id, project_id, slug, patched_cycle=patched_cycle)
        print("The response of WorkspacesApi->workspaces_projects_cycles_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_cycle** | [**PatchedCycle**](PatchedCycle.md)|  | [optional] 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_retrieve**
> Cycle workspaces_projects_cycles_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_cycles_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_cycles_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_retrieve2**
> Cycle workspaces_projects_cycles_retrieve2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to cycle.

### Example

```python
import time
import os
import plane
from plane.models.cycle import Cycle
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_cycles_retrieve2(id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_cycles_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Cycle**](Cycle.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_cycles_transfer_issues_create**
> workspaces_projects_cycles_transfer_issues_create(cycle_id, project_id, slug)



This viewset provides `create` actions for transferring the issues into a particular cycle.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    cycle_id = 'cycle_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_cycles_transfer_issues_create(cycle_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_cycles_transfer_issues_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **cycle_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_destroy**
> workspaces_projects_destroy(slug)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_destroy(slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_destroy2**
> workspaces_projects_destroy2(id, slug)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_destroy2(id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_create**
> InboxIssue workspaces_projects_inbox_issues_create(project_id, slug, inbox_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    inbox_issue = plane.InboxIssue() # InboxIssue | 

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_create(project_id, slug, inbox_issue)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **inbox_issue** | [**InboxIssue**](InboxIssue.md)|  | 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_create2**
> InboxIssue workspaces_projects_inbox_issues_create2(issue_id, project_id, slug, inbox_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    inbox_issue = plane.InboxIssue() # InboxIssue | 

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_create2(issue_id, project_id, slug, inbox_issue)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **inbox_issue** | [**InboxIssue**](InboxIssue.md)|  | 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_destroy**
> workspaces_projects_inbox_issues_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_inbox_issues_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_destroy2**
> workspaces_projects_inbox_issues_destroy2(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_inbox_issues_destroy2(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_partial_update**
> InboxIssue workspaces_projects_inbox_issues_partial_update(project_id, slug, patched_inbox_issue=patched_inbox_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.models.patched_inbox_issue import PatchedInboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_inbox_issue = plane.PatchedInboxIssue() # PatchedInboxIssue |  (optional)

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_partial_update(project_id, slug, patched_inbox_issue=patched_inbox_issue)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_inbox_issue** | [**PatchedInboxIssue**](PatchedInboxIssue.md)|  | [optional] 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_partial_update2**
> InboxIssue workspaces_projects_inbox_issues_partial_update2(issue_id, project_id, slug, patched_inbox_issue=patched_inbox_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.models.patched_inbox_issue import PatchedInboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_inbox_issue = plane.PatchedInboxIssue() # PatchedInboxIssue |  (optional)

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_partial_update2(issue_id, project_id, slug, patched_inbox_issue=patched_inbox_issue)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_inbox_issue** | [**PatchedInboxIssue**](PatchedInboxIssue.md)|  | [optional] 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_retrieve**
> InboxIssue workspaces_projects_inbox_issues_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_inbox_issues_retrieve2**
> InboxIssue workspaces_projects_inbox_issues_retrieve2(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to inbox issues.

### Example

```python
import time
import os
import plane
from plane.models.inbox_issue import InboxIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_inbox_issues_retrieve2(issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_inbox_issues_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_inbox_issues_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**InboxIssue**](InboxIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_create**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_create(project_id, property_id, slug, issue_property_option_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_property_option_api = plane.IssuePropertyOptionAPI() # IssuePropertyOptionAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_create(project_id, property_id, slug, issue_property_option_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_property_option_api** | [**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)|  | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_create2**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_create2(option_id, project_id, property_id, slug, issue_property_option_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_property_option_api = plane.IssuePropertyOptionAPI() # IssuePropertyOptionAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_create2(option_id, project_id, property_id, slug, issue_property_option_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_property_option_api** | [**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)|  | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_destroy**
> workspaces_projects_issue_properties_options_destroy(project_id, property_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issue_properties_options_destroy(project_id, property_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_destroy2**
> workspaces_projects_issue_properties_options_destroy2(option_id, project_id, property_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issue_properties_options_destroy2(option_id, project_id, property_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_partial_update**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_partial_update(project_id, property_id, slug, patched_issue_property_option_api=patched_issue_property_option_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.models.patched_issue_property_option_api import PatchedIssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_property_option_api = plane.PatchedIssuePropertyOptionAPI() # PatchedIssuePropertyOptionAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_partial_update(project_id, property_id, slug, patched_issue_property_option_api=patched_issue_property_option_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_property_option_api** | [**PatchedIssuePropertyOptionAPI**](PatchedIssuePropertyOptionAPI.md)|  | [optional] 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_partial_update2**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_partial_update2(option_id, project_id, property_id, slug, patched_issue_property_option_api=patched_issue_property_option_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.models.patched_issue_property_option_api import PatchedIssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_property_option_api = plane.PatchedIssuePropertyOptionAPI() # PatchedIssuePropertyOptionAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_partial_update2(option_id, project_id, property_id, slug, patched_issue_property_option_api=patched_issue_property_option_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_property_option_api** | [**PatchedIssuePropertyOptionAPI**](PatchedIssuePropertyOptionAPI.md)|  | [optional] 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_retrieve**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_retrieve(project_id, property_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_retrieve(project_id, property_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_properties_options_retrieve2**
> IssuePropertyOptionAPI workspaces_projects_issue_properties_options_retrieve2(option_id, project_id, property_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue property options.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_option_api import IssuePropertyOptionAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    option_id = 'option_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_properties_options_retrieve2(option_id, project_id, property_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issue_properties_options_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_properties_options_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **option_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssuePropertyOptionAPI**](IssuePropertyOptionAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_create**
> IssueTypeAPI workspaces_projects_issue_types_create(project_id, slug, issue_type_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_type_api = plane.IssueTypeAPI() # IssueTypeAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_create(project_id, slug, issue_type_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_type_api** | [**IssueTypeAPI**](IssueTypeAPI.md)|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_create2**
> IssueTypeAPI workspaces_projects_issue_types_create2(project_id, slug, type_id, issue_type_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    issue_type_api = plane.IssueTypeAPI() # IssueTypeAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_create2(project_id, slug, type_id, issue_type_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **issue_type_api** | [**IssueTypeAPI**](IssueTypeAPI.md)|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_destroy**
> workspaces_projects_issue_types_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issue_types_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_destroy2**
> workspaces_projects_issue_types_destroy2(project_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_instance.workspaces_projects_issue_types_destroy2(project_id, slug, type_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_create**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_create(project_id, slug, type_id, issue_property_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    issue_property_api = plane.IssuePropertyAPI() # IssuePropertyAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_create(project_id, slug, type_id, issue_property_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **issue_property_api** | [**IssuePropertyAPI**](IssuePropertyAPI.md)|  | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_create2**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_create2(project_id, property_id, slug, type_id, issue_property_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    issue_property_api = plane.IssuePropertyAPI() # IssuePropertyAPI | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_create2(project_id, property_id, slug, type_id, issue_property_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **issue_property_api** | [**IssuePropertyAPI**](IssuePropertyAPI.md)|  | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_destroy**
> workspaces_projects_issue_types_issue_properties_destroy(project_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_instance.workspaces_projects_issue_types_issue_properties_destroy(project_id, slug, type_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_destroy2**
> workspaces_projects_issue_types_issue_properties_destroy2(project_id, property_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_instance.workspaces_projects_issue_types_issue_properties_destroy2(project_id, property_id, slug, type_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_partial_update**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_partial_update(project_id, slug, type_id, patched_issue_property_api=patched_issue_property_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.models.patched_issue_property_api import PatchedIssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    patched_issue_property_api = plane.PatchedIssuePropertyAPI() # PatchedIssuePropertyAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_partial_update(project_id, slug, type_id, patched_issue_property_api=patched_issue_property_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **patched_issue_property_api** | [**PatchedIssuePropertyAPI**](PatchedIssuePropertyAPI.md)|  | [optional] 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_partial_update2**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_partial_update2(project_id, property_id, slug, type_id, patched_issue_property_api=patched_issue_property_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.models.patched_issue_property_api import PatchedIssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    patched_issue_property_api = plane.PatchedIssuePropertyAPI() # PatchedIssuePropertyAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_partial_update2(project_id, property_id, slug, type_id, patched_issue_property_api=patched_issue_property_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **patched_issue_property_api** | [**PatchedIssuePropertyAPI**](PatchedIssuePropertyAPI.md)|  | [optional] 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_retrieve**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_retrieve(project_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_retrieve(project_id, slug, type_id)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_issue_properties_retrieve2**
> IssuePropertyAPI workspaces_projects_issue_types_issue_properties_retrieve2(project_id, property_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue type properties.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_api import IssuePropertyAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_issue_properties_retrieve2(project_id, property_id, slug, type_id)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_issue_properties_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_issue_properties_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

[**IssuePropertyAPI**](IssuePropertyAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_partial_update**
> IssueTypeAPI workspaces_projects_issue_types_partial_update(project_id, slug, patched_issue_type_api=patched_issue_type_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.models.patched_issue_type_api import PatchedIssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_type_api = plane.PatchedIssueTypeAPI() # PatchedIssueTypeAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_types_partial_update(project_id, slug, patched_issue_type_api=patched_issue_type_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_type_api** | [**PatchedIssueTypeAPI**](PatchedIssueTypeAPI.md)|  | [optional] 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_partial_update2**
> IssueTypeAPI workspaces_projects_issue_types_partial_update2(project_id, slug, type_id, patched_issue_type_api=patched_issue_type_api)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.models.patched_issue_type_api import PatchedIssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 
    patched_issue_type_api = plane.PatchedIssueTypeAPI() # PatchedIssueTypeAPI |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issue_types_partial_update2(project_id, slug, type_id, patched_issue_type_api=patched_issue_type_api)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 
 **patched_issue_type_api** | [**PatchedIssueTypeAPI**](PatchedIssueTypeAPI.md)|  | [optional] 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_retrieve**
> IssueTypeAPI workspaces_projects_issue_types_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issue_types_retrieve2**
> IssueTypeAPI workspaces_projects_issue_types_retrieve2(project_id, slug, type_id)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue types.

### Example

```python
import time
import os
import plane
from plane.models.issue_type_api import IssueTypeAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    type_id = 'type_id_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issue_types_retrieve2(project_id, slug, type_id)
        print("The response of WorkspacesApi->workspaces_projects_issue_types_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issue_types_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **type_id** | **str**|  | 

### Return type

[**IssueTypeAPI**](IssueTypeAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_activities_retrieve**
> workspaces_projects_issues_activities_retrieve(issue_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_activities_retrieve(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_activities_retrieve: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_activities_retrieve2**
> workspaces_projects_issues_activities_retrieve2(id, issue_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_activities_retrieve2(id, issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_activities_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_create**
> IssueComment workspaces_projects_issues_comments_create(issue_id, project_id, slug, issue_comment=issue_comment)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_comment = plane.IssueComment() # IssueComment |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_comments_create(issue_id, project_id, slug, issue_comment=issue_comment)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_comment** | [**IssueComment**](IssueComment.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_create2**
> IssueComment workspaces_projects_issues_comments_create2(id, issue_id, project_id, slug, issue_comment=issue_comment)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_comment = plane.IssueComment() # IssueComment |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_comments_create2(id, issue_id, project_id, slug, issue_comment=issue_comment)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_comment** | [**IssueComment**](IssueComment.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_destroy**
> workspaces_projects_issues_comments_destroy(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_comments_destroy(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_destroy: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_destroy2**
> workspaces_projects_issues_comments_destroy2(id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_comments_destroy2(id, issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_partial_update**
> IssueComment workspaces_projects_issues_comments_partial_update(issue_id, project_id, slug, patched_issue_comment=patched_issue_comment)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.models.patched_issue_comment import PatchedIssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_comment = plane.PatchedIssueComment() # PatchedIssueComment |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_comments_partial_update(issue_id, project_id, slug, patched_issue_comment=patched_issue_comment)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_comment** | [**PatchedIssueComment**](PatchedIssueComment.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_partial_update2**
> IssueComment workspaces_projects_issues_comments_partial_update2(id, issue_id, project_id, slug, patched_issue_comment=patched_issue_comment)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.models.patched_issue_comment import PatchedIssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_comment = plane.PatchedIssueComment() # PatchedIssueComment |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_comments_partial_update2(id, issue_id, project_id, slug, patched_issue_comment=patched_issue_comment)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_comment** | [**PatchedIssueComment**](PatchedIssueComment.md)|  | [optional] 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_retrieve**
> IssueComment workspaces_projects_issues_comments_retrieve(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_comments_retrieve(issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_comments_retrieve2**
> IssueComment workspaces_projects_issues_comments_retrieve2(id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to comments of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_comment import IssueComment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_comments_retrieve2(id, issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_comments_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_comments_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueComment**](IssueComment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_create**
> Issue workspaces_projects_issues_create(project_id, slug, issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue = plane.Issue() # Issue | 

    try:
        api_response = api_instance.workspaces_projects_issues_create(project_id, slug, issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_create: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_create2**
> Issue workspaces_projects_issues_create2(id, project_id, slug, issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue = plane.Issue() # Issue | 

    try:
        api_response = api_instance.workspaces_projects_issues_create2(id, project_id, slug, issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue** | [**Issue**](Issue.md)|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_destroy**
> workspaces_projects_issues_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_destroy2**
> workspaces_projects_issues_destroy2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_destroy2(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_issue_attachments_create**
> IssueAttachment workspaces_projects_issues_issue_attachments_create(issue_id, project_id, slug, asset, created_at, id, issue, project, updated_at, updated_by, workspace, attributes=attributes, comment=comment, created_by=created_by, deleted_at=deleted_at, draft_issue=draft_issue, entity_type=entity_type, external_id=external_id, external_source=external_source, is_archived=is_archived, is_deleted=is_deleted, is_uploaded=is_uploaded, page=page, size=size, storage_metadata=storage_metadata, user=user)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.issue_attachment import IssueAttachment
from plane.models.issue_attachment_entity_type import IssueAttachmentEntityType
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    asset = 'asset_example' # str | 
    created_at = '2013-10-20T19:20:30+01:00' # datetime | 
    id = 'id_example' # str | 
    issue = 'issue_example' # str | 
    project = 'project_example' # str | 
    updated_at = '2013-10-20T19:20:30+01:00' # datetime | 
    updated_by = 'updated_by_example' # str | 
    workspace = 'workspace_example' # str | 
    attributes = None # object |  (optional)
    comment = 'comment_example' # str |  (optional)
    created_by = 'created_by_example' # str |  (optional)
    deleted_at = '2013-10-20T19:20:30+01:00' # datetime |  (optional)
    draft_issue = 'draft_issue_example' # str |  (optional)
    entity_type = plane.IssueAttachmentEntityType() # IssueAttachmentEntityType |  (optional)
    external_id = 'external_id_example' # str |  (optional)
    external_source = 'external_source_example' # str |  (optional)
    is_archived = True # bool |  (optional)
    is_deleted = True # bool |  (optional)
    is_uploaded = True # bool |  (optional)
    page = 'page_example' # str |  (optional)
    size = 3.4 # float |  (optional)
    storage_metadata = None # object |  (optional)
    user = 'user_example' # str |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_issue_attachments_create(issue_id, project_id, slug, asset, created_at, id, issue, project, updated_at, updated_by, workspace, attributes=attributes, comment=comment, created_by=created_by, deleted_at=deleted_at, draft_issue=draft_issue, entity_type=entity_type, external_id=external_id, external_source=external_source, is_archived=is_archived, is_deleted=is_deleted, is_uploaded=is_uploaded, page=page, size=size, storage_metadata=storage_metadata, user=user)
        print("The response of WorkspacesApi->workspaces_projects_issues_issue_attachments_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_issue_attachments_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **asset** | **str**|  | 
 **created_at** | **datetime**|  | 
 **id** | **str**|  | 
 **issue** | **str**|  | 
 **project** | **str**|  | 
 **updated_at** | **datetime**|  | 
 **updated_by** | **str**|  | 
 **workspace** | **str**|  | 
 **attributes** | [**object**](object.md)|  | [optional] 
 **comment** | **str**|  | [optional] 
 **created_by** | **str**|  | [optional] 
 **deleted_at** | **datetime**|  | [optional] 
 **draft_issue** | **str**|  | [optional] 
 **entity_type** | [**IssueAttachmentEntityType**](IssueAttachmentEntityType.md)|  | [optional] 
 **external_id** | **str**|  | [optional] 
 **external_source** | **str**|  | [optional] 
 **is_archived** | **bool**|  | [optional] 
 **is_deleted** | **bool**|  | [optional] 
 **is_uploaded** | **bool**|  | [optional] 
 **page** | **str**|  | [optional] 
 **size** | **float**|  | [optional] 
 **storage_metadata** | [**object**](object.md)|  | [optional] 
 **user** | **str**|  | [optional] 

### Return type

[**IssueAttachment**](IssueAttachment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_issue_attachments_destroy**
> workspaces_projects_issues_issue_attachments_destroy(issue_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_issue_attachments_destroy(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_issue_attachments_destroy: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_issue_attachments_retrieve**
> IssueAttachment workspaces_projects_issues_issue_attachments_retrieve(issue_id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.issue_attachment import IssueAttachment
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_issue_attachments_retrieve(issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_issue_attachments_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_issue_attachments_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueAttachment**](IssueAttachment.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_issue_properties_values_create**
> IssuePropertyValueAPI workspaces_projects_issues_issue_properties_values_create(issue_id, project_id, property_id, slug, issue_property_value_api)



This viewset automatically provides `list`, `create`, and `update`
actions related to issue property values.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_value_api import IssuePropertyValueAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_property_value_api = plane.IssuePropertyValueAPI() # IssuePropertyValueAPI | 

    try:
        api_response = api_instance.workspaces_projects_issues_issue_properties_values_create(issue_id, project_id, property_id, slug, issue_property_value_api)
        print("The response of WorkspacesApi->workspaces_projects_issues_issue_properties_values_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_issue_properties_values_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_property_value_api** | [**IssuePropertyValueAPI**](IssuePropertyValueAPI.md)|  | 

### Return type

[**IssuePropertyValueAPI**](IssuePropertyValueAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_issue_properties_values_retrieve**
> IssuePropertyValueAPI workspaces_projects_issues_issue_properties_values_retrieve(issue_id, project_id, property_id, slug)



This viewset automatically provides `list`, `create`, and `update`
actions related to issue property values.

### Example

```python
import time
import os
import plane
from plane.models.issue_property_value_api import IssuePropertyValueAPI
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    property_id = 'property_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_issue_properties_values_retrieve(issue_id, project_id, property_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_issue_properties_values_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_issue_properties_values_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **property_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssuePropertyValueAPI**](IssuePropertyValueAPI.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_create**
> IssueLink workspaces_projects_issues_links_create(issue_id, project_id, slug, issue_link)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_link = plane.IssueLink() # IssueLink | 

    try:
        api_response = api_instance.workspaces_projects_issues_links_create(issue_id, project_id, slug, issue_link)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_link** | [**IssueLink**](IssueLink.md)|  | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_create2**
> IssueLink workspaces_projects_issues_links_create2(id, issue_id, project_id, slug, issue_link)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue_link = plane.IssueLink() # IssueLink | 

    try:
        api_response = api_instance.workspaces_projects_issues_links_create2(id, issue_id, project_id, slug, issue_link)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue_link** | [**IssueLink**](IssueLink.md)|  | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_destroy**
> workspaces_projects_issues_links_destroy(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_links_destroy(issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_destroy: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_destroy2**
> workspaces_projects_issues_links_destroy2(id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_issues_links_destroy2(id, issue_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_partial_update**
> IssueLink workspaces_projects_issues_links_partial_update(issue_id, project_id, slug, patched_issue_link=patched_issue_link)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.models.patched_issue_link import PatchedIssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_link = plane.PatchedIssueLink() # PatchedIssueLink |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_links_partial_update(issue_id, project_id, slug, patched_issue_link=patched_issue_link)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_link** | [**PatchedIssueLink**](PatchedIssueLink.md)|  | [optional] 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_partial_update2**
> IssueLink workspaces_projects_issues_links_partial_update2(id, issue_id, project_id, slug, patched_issue_link=patched_issue_link)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.models.patched_issue_link import PatchedIssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue_link = plane.PatchedIssueLink() # PatchedIssueLink |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_links_partial_update2(id, issue_id, project_id, slug, patched_issue_link=patched_issue_link)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue_link** | [**PatchedIssueLink**](PatchedIssueLink.md)|  | [optional] 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_retrieve**
> IssueLink workspaces_projects_issues_links_retrieve(issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_links_retrieve(issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_links_retrieve2**
> IssueLink workspaces_projects_issues_links_retrieve2(id, issue_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the links of the particular issue.

### Example

```python
import time
import os
import plane
from plane.models.issue_link import IssueLink
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    issue_id = 'issue_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_links_retrieve2(id, issue_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_links_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_links_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **issue_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**IssueLink**](IssueLink.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_partial_update**
> Issue workspaces_projects_issues_partial_update(project_id, slug, patched_issue=patched_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.models.patched_issue import PatchedIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue = plane.PatchedIssue() # PatchedIssue |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_partial_update(project_id, slug, patched_issue=patched_issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_issue** | [**PatchedIssue**](PatchedIssue.md)|  | [optional] 

### Return type

[**Issue**](Issue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_partial_update2**
> Issue workspaces_projects_issues_partial_update2(id, project_id, slug, patched_issue=patched_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.models.patched_issue import PatchedIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_issue = plane.PatchedIssue() # PatchedIssue |  (optional)

    try:
        api_response = api_instance.workspaces_projects_issues_partial_update2(id, project_id, slug, patched_issue=patched_issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_partial_update2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_retrieve**
> Issue workspaces_projects_issues_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_retrieve2**
> Issue workspaces_projects_issues_retrieve2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_issues_retrieve2(id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_issues_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_update**
> Issue workspaces_projects_issues_update(project_id, slug, issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue = plane.Issue() # Issue | 

    try:
        api_response = api_instance.workspaces_projects_issues_update(project_id, slug, issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_update: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_issues_update2**
> Issue workspaces_projects_issues_update2(id, project_id, slug, issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to issue.

### Example

```python
import time
import os
import plane
from plane.models.issue import Issue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    issue = plane.Issue() # Issue | 

    try:
        api_response = api_instance.workspaces_projects_issues_update2(id, project_id, slug, issue)
        print("The response of WorkspacesApi->workspaces_projects_issues_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_issues_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **issue** | [**Issue**](Issue.md)|  | 

### Return type

[**Issue**](Issue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_create**
> Label workspaces_projects_labels_create(project_id, slug, label)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    label = plane.Label() # Label | 

    try:
        api_response = api_instance.workspaces_projects_labels_create(project_id, slug, label)
        print("The response of WorkspacesApi->workspaces_projects_labels_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **label** | [**Label**](Label.md)|  | 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_create2**
> Label workspaces_projects_labels_create2(id, project_id, slug, label)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    label = plane.Label() # Label | 

    try:
        api_response = api_instance.workspaces_projects_labels_create2(id, project_id, slug, label)
        print("The response of WorkspacesApi->workspaces_projects_labels_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **label** | [**Label**](Label.md)|  | 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_destroy**
> workspaces_projects_labels_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_labels_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_destroy2**
> workspaces_projects_labels_destroy2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_labels_destroy2(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_partial_update**
> Label workspaces_projects_labels_partial_update(project_id, slug, patched_label=patched_label)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.models.patched_label import PatchedLabel
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_label = plane.PatchedLabel() # PatchedLabel |  (optional)

    try:
        api_response = api_instance.workspaces_projects_labels_partial_update(project_id, slug, patched_label=patched_label)
        print("The response of WorkspacesApi->workspaces_projects_labels_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_label** | [**PatchedLabel**](PatchedLabel.md)|  | [optional] 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_partial_update2**
> Label workspaces_projects_labels_partial_update2(id, project_id, slug, patched_label=patched_label)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.models.patched_label import PatchedLabel
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_label = plane.PatchedLabel() # PatchedLabel |  (optional)

    try:
        api_response = api_instance.workspaces_projects_labels_partial_update2(id, project_id, slug, patched_label=patched_label)
        print("The response of WorkspacesApi->workspaces_projects_labels_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_label** | [**PatchedLabel**](PatchedLabel.md)|  | [optional] 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_retrieve**
> Label workspaces_projects_labels_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_labels_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_labels_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_labels_retrieve2**
> Label workspaces_projects_labels_retrieve2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to the labels.

### Example

```python
import time
import os
import plane
from plane.models.label import Label
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_labels_retrieve2(id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_labels_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_labels_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Label**](Label.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_members_create**
> workspaces_projects_members_create(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_members_create(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_members_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_members_retrieve**
> workspaces_projects_members_retrieve(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_members_retrieve(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_members_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_archive_create**
> workspaces_projects_modules_archive_create(id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_archive_create(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_archive_create: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_archive_destroy**
> workspaces_projects_modules_archive_destroy(id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_archive_destroy(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_archive_destroy: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_archive_retrieve**
> workspaces_projects_modules_archive_retrieve(id, project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_archive_retrieve(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_archive_retrieve: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_create**
> Module workspaces_projects_modules_create(project_id, slug, module)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    module = plane.Module() # Module | 

    try:
        api_response = api_instance.workspaces_projects_modules_create(project_id, slug, module)
        print("The response of WorkspacesApi->workspaces_projects_modules_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **module** | [**Module**](Module.md)|  | 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_create2**
> Module workspaces_projects_modules_create2(id, project_id, slug, module)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    module = plane.Module() # Module | 

    try:
        api_response = api_instance.workspaces_projects_modules_create2(id, project_id, slug, module)
        print("The response of WorkspacesApi->workspaces_projects_modules_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **module** | [**Module**](Module.md)|  | 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_destroy**
> workspaces_projects_modules_destroy(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_destroy2**
> workspaces_projects_modules_destroy2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_destroy2(id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_create**
> ModuleIssue workspaces_projects_modules_module_issues_create(module_id, project_id, slug, module_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.models.module_issue import ModuleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    module_issue = plane.ModuleIssue() # ModuleIssue | 

    try:
        api_response = api_instance.workspaces_projects_modules_module_issues_create(module_id, project_id, slug, module_issue)
        print("The response of WorkspacesApi->workspaces_projects_modules_module_issues_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **module_issue** | [**ModuleIssue**](ModuleIssue.md)|  | 

### Return type

[**ModuleIssue**](ModuleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_create2**
> ModuleIssue workspaces_projects_modules_module_issues_create2(issue_id, module_id, project_id, slug, module_issue)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.models.module_issue import ModuleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    module_issue = plane.ModuleIssue() # ModuleIssue | 

    try:
        api_response = api_instance.workspaces_projects_modules_module_issues_create2(issue_id, module_id, project_id, slug, module_issue)
        print("The response of WorkspacesApi->workspaces_projects_modules_module_issues_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **module_issue** | [**ModuleIssue**](ModuleIssue.md)|  | 

### Return type

[**ModuleIssue**](ModuleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_destroy**
> workspaces_projects_modules_module_issues_destroy(module_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_module_issues_destroy(module_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_destroy2**
> workspaces_projects_modules_module_issues_destroy2(issue_id, module_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_modules_module_issues_destroy2(issue_id, module_id, project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_destroy2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_retrieve**
> ModuleIssue workspaces_projects_modules_module_issues_retrieve(module_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.models.module_issue import ModuleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_modules_module_issues_retrieve(module_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_modules_module_issues_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**ModuleIssue**](ModuleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_module_issues_retrieve2**
> ModuleIssue workspaces_projects_modules_module_issues_retrieve2(issue_id, module_id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module issues.

### Example

```python
import time
import os
import plane
from plane.models.module_issue import ModuleIssue
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    issue_id = 'issue_id_example' # str | 
    module_id = 'module_id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_modules_module_issues_retrieve2(issue_id, module_id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_modules_module_issues_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_module_issues_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **issue_id** | **str**|  | 
 **module_id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**ModuleIssue**](ModuleIssue.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_partial_update**
> Module workspaces_projects_modules_partial_update(project_id, slug, patched_module=patched_module)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.models.patched_module import PatchedModule
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_module = plane.PatchedModule() # PatchedModule |  (optional)

    try:
        api_response = api_instance.workspaces_projects_modules_partial_update(project_id, slug, patched_module=patched_module)
        print("The response of WorkspacesApi->workspaces_projects_modules_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_module** | [**PatchedModule**](PatchedModule.md)|  | [optional] 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_partial_update2**
> Module workspaces_projects_modules_partial_update2(id, project_id, slug, patched_module=patched_module)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.models.patched_module import PatchedModule
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_module = plane.PatchedModule() # PatchedModule |  (optional)

    try:
        api_response = api_instance.workspaces_projects_modules_partial_update2(id, project_id, slug, patched_module=patched_module)
        print("The response of WorkspacesApi->workspaces_projects_modules_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_module** | [**PatchedModule**](PatchedModule.md)|  | [optional] 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_retrieve**
> Module workspaces_projects_modules_retrieve(project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_modules_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_modules_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_modules_retrieve2**
> Module workspaces_projects_modules_retrieve2(id, project_id, slug)



This viewset automatically provides `list`, `create`, `retrieve`,
`update` and `destroy` actions related to module.

### Example

```python
import time
import os
import plane
from plane.models.module import Module
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_modules_retrieve2(id, project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_modules_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_modules_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Module**](Module.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_partial_update**
> Project workspaces_projects_partial_update(slug, patched_project=patched_project)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.patched_project import PatchedProject
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    slug = 'slug_example' # str | 
    patched_project = plane.PatchedProject() # PatchedProject |  (optional)

    try:
        api_response = api_instance.workspaces_projects_partial_update(slug, patched_project=patched_project)
        print("The response of WorkspacesApi->workspaces_projects_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**|  | 
 **patched_project** | [**PatchedProject**](PatchedProject.md)|  | [optional] 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_partial_update2**
> Project workspaces_projects_partial_update2(id, slug, patched_project=patched_project)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.patched_project import PatchedProject
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    slug = 'slug_example' # str | 
    patched_project = plane.PatchedProject() # PatchedProject |  (optional)

    try:
        api_response = api_instance.workspaces_projects_partial_update2(id, slug, patched_project=patched_project)
        print("The response of WorkspacesApi->workspaces_projects_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_project** | [**PatchedProject**](PatchedProject.md)|  | [optional] 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_retrieve**
> Project workspaces_projects_retrieve(slug)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_retrieve(slug)
        print("The response of WorkspacesApi->workspaces_projects_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **slug** | **str**|  | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_retrieve2**
> Project workspaces_projects_retrieve2(id, slug)



Project Endpoints to create, update, list, retrieve and delete endpoint

### Example

```python
import time
import os
import plane
from plane.models.project import Project
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    id = 'id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_retrieve2(id, slug)
        print("The response of WorkspacesApi->workspaces_projects_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_retrieve2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**Project**](Project.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_create**
> State workspaces_projects_states_create(project_id, slug, state)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state = plane.State() # State | 

    try:
        api_response = api_instance.workspaces_projects_states_create(project_id, slug, state)
        print("The response of WorkspacesApi->workspaces_projects_states_create:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_create: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state** | [**State**](State.md)|  | 

### Return type

[**State**](State.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_create2**
> State workspaces_projects_states_create2(project_id, slug, state_id, state)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 
    state = plane.State() # State | 

    try:
        api_response = api_instance.workspaces_projects_states_create2(project_id, slug, state_id, state)
        print("The response of WorkspacesApi->workspaces_projects_states_create2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_create2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state_id** | **str**|  | 
 **state** | [**State**](State.md)|  | 

### Return type

[**State**](State.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_destroy**
> workspaces_projects_states_destroy(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_instance.workspaces_projects_states_destroy(project_id, slug)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_destroy: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_destroy2**
> workspaces_projects_states_destroy2(project_id, slug, state_id)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 

    try:
        api_instance.workspaces_projects_states_destroy2(project_id, slug, state_id)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_destroy2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No response body |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_partial_update**
> State workspaces_projects_states_partial_update(project_id, slug, patched_state=patched_state)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.patched_state import PatchedState
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    patched_state = plane.PatchedState() # PatchedState |  (optional)

    try:
        api_response = api_instance.workspaces_projects_states_partial_update(project_id, slug, patched_state=patched_state)
        print("The response of WorkspacesApi->workspaces_projects_states_partial_update:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_partial_update: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **patched_state** | [**PatchedState**](PatchedState.md)|  | [optional] 

### Return type

[**State**](State.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_partial_update2**
> State workspaces_projects_states_partial_update2(project_id, slug, state_id, patched_state=patched_state)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.patched_state import PatchedState
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 
    patched_state = plane.PatchedState() # PatchedState |  (optional)

    try:
        api_response = api_instance.workspaces_projects_states_partial_update2(project_id, slug, state_id, patched_state=patched_state)
        print("The response of WorkspacesApi->workspaces_projects_states_partial_update2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_partial_update2: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 
 **state_id** | **str**|  | 
 **patched_state** | [**PatchedState**](PatchedState.md)|  | [optional] 

### Return type

[**State**](State.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/x-www-form-urlencoded, multipart/form-data
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_retrieve**
> State workspaces_projects_states_retrieve(project_id, slug)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_states_retrieve(project_id, slug)
        print("The response of WorkspacesApi->workspaces_projects_states_retrieve:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_retrieve: %s\n" % e)
```



### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **project_id** | **str**|  | 
 **slug** | **str**|  | 

### Return type

[**State**](State.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspaces_projects_states_retrieve2**
> State workspaces_projects_states_retrieve2(project_id, slug, state_id)



This enables timezone conversion according
to the user set timezone

### Example

```python
import time
import os
import plane
from plane.models.state import State
from plane.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = plane.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with plane.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = plane.WorkspacesApi(api_client)
    project_id = 'project_id_example' # str | 
    slug = 'slug_example' # str | 
    state_id = 'state_id_example' # str | 

    try:
        api_response = api_instance.workspaces_projects_states_retrieve2(project_id, slug, state_id)
        print("The response of WorkspacesApi->workspaces_projects_states_retrieve2:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkspacesApi->workspaces_projects_states_retrieve2: %s\n" % e)
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

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** |  |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

