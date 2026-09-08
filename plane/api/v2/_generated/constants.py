"""Generated from the api_v2 OpenAPI golden (version 2.0.0) -- never hand-edited.
Source: ../plane-ee-preview/apps/api/plane/api_v2/core/schema/openapi
Regenerate: python scripts/generate_v2_constants.py <path-to>/api_v2/core/schema/openapi"""

from collections.abc import Sequence
from typing import Literal

from typing_extensions import TypedDict

API_VERSION = "2.0.0"

BULK_MAX_ITEMS = 50

OPERATION_IDS: frozenset[str] = frozenset(
    [
        "activities_list",
        "activities_retrieve",
        "assets_create",
        "assets_destroy",
        "assets_list",
        "assets_partial_update",
        "assets_retrieve",
        "attachments_create",
        "attachments_destroy",
        "attachments_list",
        "attachments_partial_update",
        "attachments_retrieve",
        "audit_logs_list",
        "audit_logs_retrieve",
        "collections_members",
        "collections_members_list",
        "collections_pages",
        "collections_pages_search",
        "comments_create",
        "comments_destroy",
        "comments_list",
        "comments_partial_update",
        "comments_retrieve",
        "customer_properties_create",
        "customer_properties_destroy",
        "customer_properties_list",
        "customer_properties_partial_update",
        "customer_properties_retrieve",
        "customer_property_values_create",
        "customer_property_values_list",
        "customer_requests_create",
        "customer_requests_destroy",
        "customer_requests_list",
        "customer_requests_partial_update",
        "customer_requests_retrieve",
        "customers_create",
        "customers_destroy",
        "customers_list",
        "customers_partial_update",
        "customers_retrieve",
        "customers_upsert",
        "customers_work_items",
        "cycles_bulk_create",
        "cycles_bulk_delete",
        "cycles_bulk_update",
        "cycles_create",
        "cycles_destroy",
        "cycles_list",
        "cycles_partial_update",
        "cycles_retrieve",
        "cycles_transfer",
        "cycles_upsert",
        "cycles_work_items_manage",
        "estimate_points_bulk_create",
        "estimate_points_bulk_delete",
        "estimate_points_bulk_update",
        "estimate_points_create",
        "estimate_points_destroy",
        "estimate_points_list",
        "estimate_points_partial_update",
        "estimate_points_retrieve",
        "estimate_points_upsert",
        "estimates_bulk_create",
        "estimates_bulk_delete",
        "estimates_bulk_update",
        "estimates_create",
        "estimates_destroy",
        "estimates_list",
        "estimates_partial_update",
        "estimates_retrieve",
        "estimates_upsert",
        "group_sync_config_retrieve",
        "group_sync_config_update",
        "group_sync_project_mappings_create",
        "group_sync_project_mappings_destroy",
        "group_sync_project_mappings_list",
        "group_sync_project_mappings_retrieve",
        "group_sync_project_mappings_update",
        "group_sync_workspace_mappings_create",
        "group_sync_workspace_mappings_destroy",
        "group_sync_workspace_mappings_list",
        "group_sync_workspace_mappings_retrieve",
        "group_sync_workspace_mappings_update",
        "initiative_labels_create",
        "initiative_labels_destroy",
        "initiative_labels_list",
        "initiative_labels_partial_update",
        "initiative_labels_retrieve",
        "initiatives_create",
        "initiatives_destroy",
        "initiatives_labels",
        "initiatives_list",
        "initiatives_partial_update",
        "initiatives_projects",
        "initiatives_retrieve",
        "initiatives_work_items",
        "intakes_create",
        "intakes_destroy",
        "intakes_list",
        "intakes_partial_update",
        "intakes_retrieve",
        "labels_bulk_create",
        "labels_bulk_delete",
        "labels_bulk_update",
        "labels_create",
        "labels_destroy",
        "labels_list",
        "labels_partial_update",
        "labels_retrieve",
        "labels_upsert",
        "links_create",
        "links_destroy",
        "links_list",
        "links_partial_update",
        "links_retrieve",
        "members_bulk",
        "members_create",
        "members_destroy",
        "members_list",
        "members_retrieve",
        "milestones_bulk_create",
        "milestones_bulk_delete",
        "milestones_bulk_update",
        "milestones_create",
        "milestones_destroy",
        "milestones_list",
        "milestones_partial_update",
        "milestones_retrieve",
        "milestones_upsert",
        "milestones_work_items",
        "modules_bulk_create",
        "modules_bulk_delete",
        "modules_bulk_update",
        "modules_create",
        "modules_destroy",
        "modules_list",
        "modules_partial_update",
        "modules_retrieve",
        "modules_upsert",
        "modules_work_items_manage",
        "pages_create",
        "pages_destroy",
        "pages_list",
        "pages_partial_update",
        "pages_retrieve",
        "permission_schemes_list",
        "permission_schemes_retrieve",
        "project_automation_activities_list",
        "project_automation_activities_retrieve",
        "project_automation_edges_create",
        "project_automation_edges_destroy",
        "project_automation_edges_list",
        "project_automation_edges_partial_update",
        "project_automation_edges_retrieve",
        "project_automation_nodes_create",
        "project_automation_nodes_destroy",
        "project_automation_nodes_list",
        "project_automation_nodes_partial_update",
        "project_automation_nodes_regenerate_webhook_secret",
        "project_automation_nodes_retrieve",
        "project_automations_create",
        "project_automations_destroy",
        "project_automations_list",
        "project_automations_partial_update",
        "project_automations_retrieve",
        "project_automations_status",
        "project_features_retrieve",
        "project_features_update",
        "project_members_create",
        "project_members_destroy",
        "project_members_list",
        "project_members_partial_update",
        "project_members_retrieve",
        "project_pages_create",
        "project_pages_destroy",
        "project_pages_list",
        "project_pages_partial_update",
        "project_pages_retrieve",
        "project_role_distribution",
        "project_views_create",
        "project_views_destroy",
        "project_views_list",
        "project_views_partial_update",
        "project_views_retrieve",
        "project_work_item_templates_create",
        "project_work_item_templates_destroy",
        "project_work_item_templates_list",
        "project_work_item_templates_partial_update",
        "project_work_item_templates_retrieve",
        "project_worklogs_summary",
        "projects_archive",
        "projects_bulk_create",
        "projects_bulk_update",
        "projects_create",
        "projects_destroy",
        "projects_list",
        "projects_partial_update",
        "projects_retrieve",
        "projects_summary",
        "projects_unarchive",
        "projects_upsert",
        "release_comments_create",
        "release_comments_destroy",
        "release_comments_list",
        "release_comments_partial_update",
        "release_comments_retrieve",
        "release_labels_create",
        "release_labels_destroy",
        "release_labels_list",
        "release_labels_partial_update",
        "release_labels_retrieve",
        "release_links_create",
        "release_links_destroy",
        "release_links_list",
        "release_links_partial_update",
        "release_links_retrieve",
        "release_tags_create",
        "release_tags_destroy",
        "release_tags_list",
        "release_tags_partial_update",
        "release_tags_retrieve",
        "releases_changelog_partial_update",
        "releases_changelog_retrieve",
        "releases_create",
        "releases_destroy",
        "releases_labels",
        "releases_list",
        "releases_partial_update",
        "releases_retrieve",
        "releases_work_items",
        "roles_list",
        "roles_retrieve",
        "states_bulk_create",
        "states_bulk_delete",
        "states_bulk_update",
        "states_create",
        "states_destroy",
        "states_list",
        "states_partial_update",
        "states_retrieve",
        "states_upsert",
        "stickies_create",
        "stickies_destroy",
        "stickies_list",
        "stickies_partial_update",
        "stickies_retrieve",
        "teamspaces_create",
        "teamspaces_destroy",
        "teamspaces_list",
        "teamspaces_partial_update",
        "teamspaces_retrieve",
        "user_assets_create",
        "user_assets_destroy",
        "user_assets_list",
        "user_assets_partial_update",
        "user_assets_retrieve",
        "users_me_retrieve",
        "webhook_logs_list",
        "webhook_logs_retrieve",
        "webhooks_create",
        "webhooks_destroy",
        "webhooks_list",
        "webhooks_partial_update",
        "webhooks_regenerate",
        "webhooks_retrieve",
        "work_item_comments_bulk_create",
        "work_item_comments_bulk_delete",
        "work_item_comments_bulk_update",
        "work_item_comments_upsert",
        "work_item_dependencies_create",
        "work_item_dependencies_destroy",
        "work_item_dependencies_list",
        "work_item_properties_create",
        "work_item_properties_destroy",
        "work_item_properties_list",
        "work_item_properties_partial_update",
        "work_item_properties_retrieve",
        "work_item_property_contexts_create",
        "work_item_property_contexts_destroy",
        "work_item_property_contexts_list",
        "work_item_property_contexts_partial_update",
        "work_item_property_contexts_retrieve",
        "work_item_property_options_create",
        "work_item_property_options_destroy",
        "work_item_property_options_list",
        "work_item_property_options_partial_update",
        "work_item_property_options_retrieve",
        "work_item_relation_definitions_create",
        "work_item_relation_definitions_destroy",
        "work_item_relation_definitions_list",
        "work_item_relation_definitions_partial_update",
        "work_item_relation_definitions_retrieve",
        "work_item_relations_create",
        "work_item_relations_destroy",
        "work_item_relations_list",
        "work_item_type_properties_attach",
        "work_item_type_properties_detach",
        "work_item_type_properties_list",
        "work_item_type_properties_retrieve",
        "work_item_types_create",
        "work_item_types_destroy",
        "work_item_types_enable",
        "work_item_types_import",
        "work_item_types_list",
        "work_item_types_mark_default",
        "work_item_types_partial_update",
        "work_item_types_retrieve",
        "work_item_types_schema",
        "work_items_archive",
        "work_items_bulk_create",
        "work_items_bulk_delete",
        "work_items_bulk_update",
        "work_items_create",
        "work_items_destroy",
        "work_items_list",
        "work_items_partial_update",
        "work_items_retrieve",
        "work_items_retrieve_by_identifier",
        "work_items_unarchive",
        "work_items_upsert",
        "work_items_use",
        "workflow_states_create",
        "workflow_states_destroy",
        "workflow_states_list",
        "workflow_states_partial_update",
        "workflow_states_retrieve",
        "workflow_transitions_create",
        "workflow_transitions_destroy",
        "workflow_transitions_list",
        "workflow_transitions_partial_update",
        "workflow_transitions_retrieve",
        "workflows_create",
        "workflows_destroy",
        "workflows_list",
        "workflows_partial_update",
        "workflows_retrieve",
        "worklogs_create",
        "worklogs_destroy",
        "worklogs_list",
        "worklogs_partial_update",
        "worklogs_retrieve",
        "workspace_automation_activities_list",
        "workspace_automation_activities_retrieve",
        "workspace_automation_edges_create",
        "workspace_automation_edges_destroy",
        "workspace_automation_edges_list",
        "workspace_automation_edges_partial_update",
        "workspace_automation_edges_retrieve",
        "workspace_automation_nodes_create",
        "workspace_automation_nodes_destroy",
        "workspace_automation_nodes_list",
        "workspace_automation_nodes_partial_update",
        "workspace_automation_nodes_regenerate_webhook_secret",
        "workspace_automation_nodes_retrieve",
        "workspace_automations_create",
        "workspace_automations_destroy",
        "workspace_automations_list",
        "workspace_automations_partial_update",
        "workspace_automations_retrieve",
        "workspace_automations_status",
        "workspace_features_retrieve",
        "workspace_features_update",
        "workspace_members_list",
        "workspace_members_remove",
        "workspace_pages_create",
        "workspace_pages_destroy",
        "workspace_pages_list",
        "workspace_pages_partial_update",
        "workspace_pages_retrieve",
        "workspace_views_create",
        "workspace_views_destroy",
        "workspace_views_list",
        "workspace_views_partial_update",
        "workspace_views_retrieve",
        "workspace_work_item_properties_create",
        "workspace_work_item_properties_destroy",
        "workspace_work_item_properties_list",
        "workspace_work_item_properties_partial_update",
        "workspace_work_item_properties_retrieve",
        "workspace_work_item_property_options_create",
        "workspace_work_item_property_options_destroy",
        "workspace_work_item_property_options_list",
        "workspace_work_item_property_options_partial_update",
        "workspace_work_item_property_options_retrieve",
        "workspace_work_item_templates_create",
        "workspace_work_item_templates_destroy",
        "workspace_work_item_templates_list",
        "workspace_work_item_templates_partial_update",
        "workspace_work_item_templates_retrieve",
        "workspace_work_item_type_properties_attach",
        "workspace_work_item_type_properties_detach",
        "workspace_work_item_type_properties_list",
        "workspace_work_item_type_properties_retrieve",
        "workspace_work_item_types_create",
        "workspace_work_item_types_destroy",
        "workspace_work_item_types_list",
        "workspace_work_item_types_mark_default",
        "workspace_work_item_types_partial_update",
        "workspace_work_item_types_retrieve",
        "workspace_work_items_list",
        "workspaces_artifacts_create",
        "workspaces_artifacts_publish_create",
        "workspaces_artifacts_retrieve",
        "workspaces_artifacts_update_partial_update",
        "workspaces_permissions_me_retrieve",
        "workspaces_projects_permissions_me_retrieve",
        "workspaces_retrieve",
    ]
)

FIELDS: dict[str, frozenset[str]] = {
    "activities_list": frozenset(
        [
            "actor_id",
            "all",
            "comment",
            "created_at",
            "duration",
            "epoch",
            "external_id",
            "external_source",
            "field",
            "id",
            "issue_comment_id",
            "new_identifier_id",
            "new_value",
            "old_identifier_id",
            "old_value",
            "verb",
            "work_item_id",
        ]
    ),
    "activities_retrieve": frozenset(
        [
            "actor_id",
            "all",
            "comment",
            "created_at",
            "duration",
            "epoch",
            "external_id",
            "external_source",
            "field",
            "id",
            "issue_comment_id",
            "new_identifier_id",
            "new_value",
            "old_identifier_id",
            "old_value",
            "verb",
            "work_item_id",
        ]
    ),
    "assets_create": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
        ]
    ),
    "assets_destroy": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
        ]
    ),
    "assets_list": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
        ]
    ),
    "assets_partial_update": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
        ]
    ),
    "assets_retrieve": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
        ]
    ),
    "attachments_create": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
            "work_item_id",
        ]
    ),
    "attachments_destroy": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
            "work_item_id",
        ]
    ),
    "attachments_list": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
            "work_item_id",
        ]
    ),
    "attachments_partial_update": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
            "work_item_id",
        ]
    ),
    "attachments_retrieve": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "is_uploaded",
            "name",
            "size",
            "work_item_id",
        ]
    ),
    "audit_logs_list": frozenset(
        [
            "actor_display_name",
            "actor_email",
            "actor_id",
            "actor_type",
            "all",
            "category",
            "created_at",
            "event_id",
            "event_name",
            "id",
            "ip_address",
            "metadata",
            "new_value",
            "old_value",
            "outcome",
            "project_id",
            "reason",
            "sequence_number",
            "source",
            "target_display_name",
            "target_id",
            "target_type",
            "user_agent",
            "workspace_id",
        ]
    ),
    "audit_logs_retrieve": frozenset(
        [
            "actor_display_name",
            "actor_email",
            "actor_id",
            "actor_type",
            "all",
            "category",
            "created_at",
            "event_id",
            "event_name",
            "id",
            "ip_address",
            "metadata",
            "new_value",
            "old_value",
            "outcome",
            "project_id",
            "reason",
            "sequence_number",
            "source",
            "target_display_name",
            "target_id",
            "target_type",
            "user_agent",
            "workspace_id",
        ]
    ),
    "collections_members_list": frozenset(
        [
            "access",
            "all",
            "collection_id",
            "created_at",
            "created_by_id",
            "id",
            "member_id",
            "source",
        ]
    ),
    "collections_pages_search": frozenset(["all", "id", "logo_props", "name"]),
    "comments_create": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "comments_destroy": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "comments_list": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "comments_partial_update": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "comments_retrieve": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "customer_properties_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "sort_order",
            "validation_rules",
        ]
    ),
    "customer_properties_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "sort_order",
            "validation_rules",
        ]
    ),
    "customer_properties_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "sort_order",
            "validation_rules",
        ]
    ),
    "customer_properties_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "sort_order",
            "validation_rules",
        ]
    ),
    "customer_properties_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "sort_order",
            "validation_rules",
        ]
    ),
    "customer_requests_create": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "customer_id",
            "description",
            "description_html",
            "id",
            "link",
            "name",
        ]
    ),
    "customer_requests_destroy": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "customer_id",
            "description",
            "description_html",
            "id",
            "link",
            "name",
        ]
    ),
    "customer_requests_list": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "customer_id",
            "description",
            "description_html",
            "id",
            "link",
            "name",
        ]
    ),
    "customer_requests_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "customer_id",
            "description",
            "description_html",
            "id",
            "link",
            "name",
        ]
    ),
    "customer_requests_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "customer_id",
            "description",
            "description_html",
            "id",
            "link",
            "name",
        ]
    ),
    "customers_create": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "customers_destroy": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "customers_list": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "customers_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "customers_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "customers_upsert": frozenset(
        [
            "all",
            "archived_at",
            "contract_status",
            "created_at",
            "created_by_id",
            "customer_request_count",
            "description",
            "description_html",
            "domain",
            "email",
            "employees",
            "external_id",
            "external_source",
            "id",
            "logo_asset_id",
            "logo_props",
            "logo_url",
            "name",
            "revenue",
            "stage",
            "website_url",
        ]
    ),
    "cycles_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "cycles_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "cycles_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "cycles_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "cycles_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "cycles_upsert": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "end_date",
            "external_id",
            "external_source",
            "id",
            "logo_props",
            "name",
            "owned_by_id",
            "sort_order",
            "start_date",
            "timezone",
        ]
    ),
    "estimate_points_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimate_points_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimate_points_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimate_points_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimate_points_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimate_points_upsert": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "estimate_id",
            "external_id",
            "external_source",
            "id",
            "key",
            "value",
        ]
    ),
    "estimates_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "estimates_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "estimates_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "estimates_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "estimates_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "estimates_upsert": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "last_used",
            "name",
            "type",
        ]
    ),
    "group_sync_project_mappings_create": frozenset(
        ["all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"]
    ),
    "group_sync_project_mappings_destroy": frozenset(
        ["all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"]
    ),
    "group_sync_project_mappings_list": frozenset(
        ["all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"]
    ),
    "group_sync_project_mappings_retrieve": frozenset(
        ["all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"]
    ),
    "group_sync_project_mappings_update": frozenset(
        ["all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"]
    ),
    "group_sync_workspace_mappings_create": frozenset(
        ["all", "created_at", "id", "idp_group_name", "role_slug"]
    ),
    "group_sync_workspace_mappings_destroy": frozenset(
        ["all", "created_at", "id", "idp_group_name", "role_slug"]
    ),
    "group_sync_workspace_mappings_list": frozenset(
        ["all", "created_at", "id", "idp_group_name", "role_slug"]
    ),
    "group_sync_workspace_mappings_retrieve": frozenset(
        ["all", "created_at", "id", "idp_group_name", "role_slug"]
    ),
    "group_sync_workspace_mappings_update": frozenset(
        ["all", "created_at", "id", "idp_group_name", "role_slug"]
    ),
    "initiative_labels_create": frozenset(
        ["all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"]
    ),
    "initiative_labels_destroy": frozenset(
        ["all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"]
    ),
    "initiative_labels_list": frozenset(
        ["all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"]
    ),
    "initiative_labels_partial_update": frozenset(
        ["all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"]
    ),
    "initiative_labels_retrieve": frozenset(
        ["all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"]
    ),
    "initiatives_create": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "description_html",
            "end_date",
            "id",
            "label_ids",
            "lead_id",
            "logo_props",
            "name",
            "project_ids",
            "start_date",
            "state",
        ]
    ),
    "initiatives_destroy": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "description_html",
            "end_date",
            "id",
            "label_ids",
            "lead_id",
            "logo_props",
            "name",
            "project_ids",
            "start_date",
            "state",
        ]
    ),
    "initiatives_list": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "description_html",
            "end_date",
            "id",
            "label_ids",
            "lead_id",
            "logo_props",
            "name",
            "project_ids",
            "start_date",
            "state",
        ]
    ),
    "initiatives_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "description_html",
            "end_date",
            "id",
            "label_ids",
            "lead_id",
            "logo_props",
            "name",
            "project_ids",
            "start_date",
            "state",
        ]
    ),
    "initiatives_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "description_html",
            "end_date",
            "id",
            "label_ids",
            "lead_id",
            "logo_props",
            "name",
            "project_ids",
            "start_date",
            "state",
        ]
    ),
    "intakes_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "duplicate_to_id",
            "external_id",
            "external_source",
            "id",
            "intake_id",
            "name",
            "priority",
            "snoozed_till",
            "source",
            "source_email",
            "state_id",
            "status",
            "work_item_id",
        ]
    ),
    "intakes_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "duplicate_to_id",
            "external_id",
            "external_source",
            "id",
            "intake_id",
            "name",
            "priority",
            "snoozed_till",
            "source",
            "source_email",
            "state_id",
            "status",
            "work_item_id",
        ]
    ),
    "intakes_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "duplicate_to_id",
            "external_id",
            "external_source",
            "id",
            "intake_id",
            "name",
            "priority",
            "snoozed_till",
            "source",
            "source_email",
            "state_id",
            "status",
            "work_item_id",
        ]
    ),
    "intakes_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "duplicate_to_id",
            "external_id",
            "external_source",
            "id",
            "intake_id",
            "name",
            "priority",
            "snoozed_till",
            "source",
            "source_email",
            "state_id",
            "status",
            "work_item_id",
        ]
    ),
    "intakes_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "duplicate_to_id",
            "external_id",
            "external_source",
            "id",
            "intake_id",
            "name",
            "priority",
            "snoozed_till",
            "source",
            "source_email",
            "state_id",
            "status",
            "work_item_id",
        ]
    ),
    "labels_create": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "labels_destroy": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "labels_list": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "labels_partial_update": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "labels_retrieve": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "labels_upsert": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "name",
            "parent_id",
            "sort_order",
        ]
    ),
    "links_create": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"]
    ),
    "links_destroy": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"]
    ),
    "links_list": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"]
    ),
    "links_partial_update": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"]
    ),
    "links_retrieve": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"]
    ),
    "members_bulk": frozenset(
        [
            "accepted",
            "all",
            "created_at",
            "created_by_id",
            "email",
            "id",
            "message",
            "responded_at",
            "role",
        ]
    ),
    "members_create": frozenset(
        [
            "accepted",
            "all",
            "created_at",
            "created_by_id",
            "email",
            "id",
            "message",
            "responded_at",
            "role",
        ]
    ),
    "members_destroy": frozenset(
        [
            "accepted",
            "all",
            "created_at",
            "created_by_id",
            "email",
            "id",
            "message",
            "responded_at",
            "role",
        ]
    ),
    "members_list": frozenset(
        [
            "accepted",
            "all",
            "created_at",
            "created_by_id",
            "email",
            "id",
            "message",
            "responded_at",
            "role",
        ]
    ),
    "members_retrieve": frozenset(
        [
            "accepted",
            "all",
            "created_at",
            "created_by_id",
            "email",
            "id",
            "message",
            "responded_at",
            "role",
        ]
    ),
    "milestones_create": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "milestones_destroy": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "milestones_list": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "milestones_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "milestones_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "milestones_upsert": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "external_id",
            "external_source",
            "id",
            "target_date",
            "title",
        ]
    ),
    "modules_create": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "modules_destroy": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "modules_list": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "modules_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "modules_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "modules_upsert": frozenset(
        [
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "sort_order",
            "start_date",
            "status",
            "target_date",
        ]
    ),
    "pages_create": frozenset(
        [
            "access",
            "all",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "is_global",
            "logo_props",
            "name",
            "owned_by_id",
            "page_ids",
            "sort_order",
        ]
    ),
    "pages_destroy": frozenset(
        [
            "access",
            "all",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "is_global",
            "logo_props",
            "name",
            "owned_by_id",
            "page_ids",
            "sort_order",
        ]
    ),
    "pages_list": frozenset(
        [
            "access",
            "all",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "is_global",
            "logo_props",
            "name",
            "owned_by_id",
            "page_ids",
            "sort_order",
        ]
    ),
    "pages_partial_update": frozenset(
        [
            "access",
            "all",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "is_global",
            "logo_props",
            "name",
            "owned_by_id",
            "page_ids",
            "sort_order",
        ]
    ),
    "pages_retrieve": frozenset(
        [
            "access",
            "all",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "is_global",
            "logo_props",
            "name",
            "owned_by_id",
            "page_ids",
            "sort_order",
        ]
    ),
    "permission_schemes_list": frozenset(
        [
            "all",
            "description",
            "id",
            "is_system",
            "name",
            "namespace",
            "permissions",
            "slug",
            "sort_order",
        ]
    ),
    "permission_schemes_retrieve": frozenset(
        [
            "all",
            "description",
            "id",
            "is_system",
            "name",
            "namespace",
            "permissions",
            "slug",
            "sort_order",
        ]
    ),
    "project_automation_activities_list": frozenset(
        [
            "actor_id",
            "all",
            "automation_edge_id",
            "automation_id",
            "automation_node_id",
            "automation_run_id",
            "automation_scope",
            "automation_version_id",
            "created_at",
            "epoch",
            "field",
            "id",
            "new_identifier",
            "new_value",
            "node_execution_id",
            "old_identifier",
            "old_value",
            "verb",
        ]
    ),
    "project_automation_activities_retrieve": frozenset(
        [
            "actor_id",
            "all",
            "automation_edge_id",
            "automation_id",
            "automation_node_id",
            "automation_run_id",
            "automation_scope",
            "automation_version_id",
            "created_at",
            "epoch",
            "field",
            "id",
            "new_identifier",
            "new_value",
            "node_execution_id",
            "old_identifier",
            "old_value",
            "verb",
        ]
    ),
    "project_automation_edges_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_edges_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_edges_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_edges_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_edges_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_nodes_create": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_nodes_destroy": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_nodes_list": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_nodes_partial_update": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automation_nodes_retrieve": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "project_automations_create": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "project_automations_destroy": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "project_automations_list": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "project_automations_partial_update": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "project_automations_retrieve": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "project_members_create": frozenset(["all", "id", "member_id", "role"]),
    "project_members_destroy": frozenset(["all", "id", "member_id", "role"]),
    "project_members_list": frozenset(["all", "id", "member_id", "role"]),
    "project_members_partial_update": frozenset(["all", "id", "member_id", "role"]),
    "project_members_retrieve": frozenset(["all", "id", "member_id", "role"]),
    "project_pages_create": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "project_pages_destroy": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "project_pages_list": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "project_pages_partial_update": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "project_pages_retrieve": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "project_views_create": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "project_views_destroy": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "project_views_list": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "project_views_partial_update": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "project_views_retrieve": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "project_work_item_templates_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "project_work_item_templates_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "project_work_item_templates_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "project_work_item_templates_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "project_work_item_templates_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "projects_create": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "projects_destroy": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "projects_list": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "projects_partial_update": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "projects_retrieve": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "projects_upsert": frozenset(
        [
            "all",
            "archive_in",
            "archived_at",
            "close_in",
            "cover_image",
            "cover_image_url",
            "created_at",
            "created_by_id",
            "cycle_view",
            "default_assignee_id",
            "default_state_id",
            "description",
            "emoji",
            "estimate_id",
            "external_id",
            "external_source",
            "guest_view_all_features",
            "icon_prop",
            "id",
            "identifier",
            "intake_view",
            "is_issue_type_enabled",
            "is_time_tracking_enabled",
            "issue_views_view",
            "logo_props",
            "module_view",
            "name",
            "network",
            "page_view",
            "priority",
            "project_lead_id",
            "start_date",
            "state_id",
            "target_date",
            "timezone",
        ]
    ),
    "release_comments_create": frozenset(
        [
            "all",
            "comment_html",
            "comment_id",
            "created_at",
            "created_by_id",
            "edited_at",
            "id",
            "is_hidden",
            "is_resolved",
            "parent_id",
            "release_id",
        ]
    ),
    "release_comments_destroy": frozenset(
        [
            "all",
            "comment_html",
            "comment_id",
            "created_at",
            "created_by_id",
            "edited_at",
            "id",
            "is_hidden",
            "is_resolved",
            "parent_id",
            "release_id",
        ]
    ),
    "release_comments_list": frozenset(
        [
            "all",
            "comment_html",
            "comment_id",
            "created_at",
            "created_by_id",
            "edited_at",
            "id",
            "is_hidden",
            "is_resolved",
            "parent_id",
            "release_id",
        ]
    ),
    "release_comments_partial_update": frozenset(
        [
            "all",
            "comment_html",
            "comment_id",
            "created_at",
            "created_by_id",
            "edited_at",
            "id",
            "is_hidden",
            "is_resolved",
            "parent_id",
            "release_id",
        ]
    ),
    "release_comments_retrieve": frozenset(
        [
            "all",
            "comment_html",
            "comment_id",
            "created_at",
            "created_by_id",
            "edited_at",
            "id",
            "is_hidden",
            "is_resolved",
            "parent_id",
            "release_id",
        ]
    ),
    "release_labels_create": frozenset(
        ["all", "color", "created_at", "created_by_id", "id", "name", "sort_order"]
    ),
    "release_labels_destroy": frozenset(
        ["all", "color", "created_at", "created_by_id", "id", "name", "sort_order"]
    ),
    "release_labels_list": frozenset(
        ["all", "color", "created_at", "created_by_id", "id", "name", "sort_order"]
    ),
    "release_labels_partial_update": frozenset(
        ["all", "color", "created_at", "created_by_id", "id", "name", "sort_order"]
    ),
    "release_labels_retrieve": frozenset(
        ["all", "color", "created_at", "created_by_id", "id", "name", "sort_order"]
    ),
    "release_links_create": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"]
    ),
    "release_links_destroy": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"]
    ),
    "release_links_list": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"]
    ),
    "release_links_partial_update": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"]
    ),
    "release_links_retrieve": frozenset(
        ["all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"]
    ),
    "release_tags_create": frozenset(
        [
            "all",
            "commit_hash",
            "created_at",
            "created_by_id",
            "description",
            "git_tag",
            "id",
            "version",
        ]
    ),
    "release_tags_destroy": frozenset(
        [
            "all",
            "commit_hash",
            "created_at",
            "created_by_id",
            "description",
            "git_tag",
            "id",
            "version",
        ]
    ),
    "release_tags_list": frozenset(
        [
            "all",
            "commit_hash",
            "created_at",
            "created_by_id",
            "description",
            "git_tag",
            "id",
            "version",
        ]
    ),
    "release_tags_partial_update": frozenset(
        [
            "all",
            "commit_hash",
            "created_at",
            "created_by_id",
            "description",
            "git_tag",
            "id",
            "version",
        ]
    ),
    "release_tags_retrieve": frozenset(
        [
            "all",
            "commit_hash",
            "created_at",
            "created_by_id",
            "description",
            "git_tag",
            "id",
            "version",
        ]
    ),
    "releases_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "description_id",
            "external_id",
            "external_source",
            "id",
            "is_latest",
            "is_prerelease",
            "label_ids",
            "lead_id",
            "name",
            "release_date",
            "status",
            "tag_id",
            "target_date",
        ]
    ),
    "releases_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "description_id",
            "external_id",
            "external_source",
            "id",
            "is_latest",
            "is_prerelease",
            "label_ids",
            "lead_id",
            "name",
            "release_date",
            "status",
            "tag_id",
            "target_date",
        ]
    ),
    "releases_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "description_id",
            "external_id",
            "external_source",
            "id",
            "is_latest",
            "is_prerelease",
            "label_ids",
            "lead_id",
            "name",
            "release_date",
            "status",
            "tag_id",
            "target_date",
        ]
    ),
    "releases_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "description_id",
            "external_id",
            "external_source",
            "id",
            "is_latest",
            "is_prerelease",
            "label_ids",
            "lead_id",
            "name",
            "release_date",
            "status",
            "tag_id",
            "target_date",
        ]
    ),
    "releases_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "description_id",
            "external_id",
            "external_source",
            "id",
            "is_latest",
            "is_prerelease",
            "label_ids",
            "lead_id",
            "name",
            "release_date",
            "status",
            "tag_id",
            "target_date",
        ]
    ),
    "roles_list": frozenset(
        ["all", "description", "id", "is_system", "level", "name", "namespace", "slug", "status"]
    ),
    "roles_retrieve": frozenset(
        ["all", "description", "id", "is_system", "level", "name", "namespace", "slug", "status"]
    ),
    "states_create": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "states_destroy": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "states_list": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "states_partial_update": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "states_retrieve": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "states_upsert": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "group",
            "id",
            "is_default",
            "is_triage",
            "name",
            "sequence",
        ]
    ),
    "stickies_create": frozenset(
        [
            "all",
            "background_color",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "id",
            "logo_props",
            "name",
            "owner_id",
            "sort_order",
        ]
    ),
    "stickies_destroy": frozenset(
        [
            "all",
            "background_color",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "id",
            "logo_props",
            "name",
            "owner_id",
            "sort_order",
        ]
    ),
    "stickies_list": frozenset(
        [
            "all",
            "background_color",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "id",
            "logo_props",
            "name",
            "owner_id",
            "sort_order",
        ]
    ),
    "stickies_partial_update": frozenset(
        [
            "all",
            "background_color",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "id",
            "logo_props",
            "name",
            "owner_id",
            "sort_order",
        ]
    ),
    "stickies_retrieve": frozenset(
        [
            "all",
            "background_color",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "id",
            "logo_props",
            "name",
            "owner_id",
            "sort_order",
        ]
    ),
    "teamspaces_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "project_ids",
        ]
    ),
    "teamspaces_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "project_ids",
        ]
    ),
    "teamspaces_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "project_ids",
        ]
    ),
    "teamspaces_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "project_ids",
        ]
    ),
    "teamspaces_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "lead_id",
            "logo_props",
            "member_ids",
            "name",
            "project_ids",
        ]
    ),
    "user_assets_create": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "id",
            "is_uploaded",
            "name",
            "size",
            "user_id",
        ]
    ),
    "user_assets_destroy": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "id",
            "is_uploaded",
            "name",
            "size",
            "user_id",
        ]
    ),
    "user_assets_list": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "id",
            "is_uploaded",
            "name",
            "size",
            "user_id",
        ]
    ),
    "user_assets_partial_update": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "id",
            "is_uploaded",
            "name",
            "size",
            "user_id",
        ]
    ),
    "user_assets_retrieve": frozenset(
        [
            "all",
            "asset_url",
            "attributes",
            "content_type",
            "created_at",
            "created_by_id",
            "entity_type",
            "id",
            "is_uploaded",
            "name",
            "size",
            "user_id",
        ]
    ),
    "webhook_logs_list": frozenset(
        [
            "all",
            "created_at",
            "duration_ms",
            "error_message",
            "event_type",
            "id",
            "request_body",
            "request_headers",
            "request_method",
            "response_body",
            "response_headers",
            "response_status",
            "retry_count",
            "status_text",
            "webhook_id",
        ]
    ),
    "webhook_logs_retrieve": frozenset(
        [
            "all",
            "created_at",
            "duration_ms",
            "error_message",
            "event_type",
            "id",
            "request_body",
            "request_headers",
            "request_method",
            "response_body",
            "response_headers",
            "response_status",
            "retry_count",
            "status_text",
            "webhook_id",
        ]
    ),
    "webhooks_create": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "url",
            "version",
        ]
    ),
    "webhooks_destroy": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "url",
            "version",
        ]
    ),
    "webhooks_list": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "url",
            "version",
        ]
    ),
    "webhooks_partial_update": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "url",
            "version",
        ]
    ),
    "webhooks_regenerate": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "secret_key",
            "url",
            "version",
        ]
    ),
    "webhooks_retrieve": frozenset(
        [
            "all",
            "content_type",
            "created_at",
            "created_by_id",
            "id",
            "is_active",
            "name",
            "scopes",
            "url",
            "version",
        ]
    ),
    "work_item_comments_upsert": frozenset(
        [
            "access",
            "actor_id",
            "all",
            "comment_html",
            "comment_stripped",
            "created_at",
            "created_by_id",
            "edited_at",
            "external_id",
            "external_source",
            "id",
            "work_item_id",
        ]
    ),
    "work_item_properties_create": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_properties_destroy": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_properties_list": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_properties_partial_update": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_properties_retrieve": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_property_contexts_create": frozenset(
        [
            "all",
            "applies_to_all_projects",
            "applies_to_all_work_item_types",
            "created_at",
            "default_value",
            "external_id",
            "external_source",
            "id",
            "is_default",
            "is_multi",
            "is_required",
            "issue_type_ids",
            "name",
            "options",
            "project_ids",
            "settings",
            "sort_order",
        ]
    ),
    "work_item_property_contexts_destroy": frozenset(
        [
            "all",
            "applies_to_all_projects",
            "applies_to_all_work_item_types",
            "created_at",
            "default_value",
            "external_id",
            "external_source",
            "id",
            "is_default",
            "is_multi",
            "is_required",
            "issue_type_ids",
            "name",
            "options",
            "project_ids",
            "settings",
            "sort_order",
        ]
    ),
    "work_item_property_contexts_list": frozenset(
        [
            "all",
            "applies_to_all_projects",
            "applies_to_all_work_item_types",
            "created_at",
            "default_value",
            "external_id",
            "external_source",
            "id",
            "is_default",
            "is_multi",
            "is_required",
            "issue_type_ids",
            "name",
            "options",
            "project_ids",
            "settings",
            "sort_order",
        ]
    ),
    "work_item_property_contexts_partial_update": frozenset(
        [
            "all",
            "applies_to_all_projects",
            "applies_to_all_work_item_types",
            "created_at",
            "default_value",
            "external_id",
            "external_source",
            "id",
            "is_default",
            "is_multi",
            "is_required",
            "issue_type_ids",
            "name",
            "options",
            "project_ids",
            "settings",
            "sort_order",
        ]
    ),
    "work_item_property_contexts_retrieve": frozenset(
        [
            "all",
            "applies_to_all_projects",
            "applies_to_all_work_item_types",
            "created_at",
            "default_value",
            "external_id",
            "external_source",
            "id",
            "is_default",
            "is_multi",
            "is_required",
            "issue_type_ids",
            "name",
            "options",
            "project_ids",
            "settings",
            "sort_order",
        ]
    ),
    "work_item_relation_definitions_create": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "inward",
            "is_active",
            "is_default",
            "logo_props",
            "name",
            "outward",
            "sort_order",
        ]
    ),
    "work_item_relation_definitions_destroy": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "inward",
            "is_active",
            "is_default",
            "logo_props",
            "name",
            "outward",
            "sort_order",
        ]
    ),
    "work_item_relation_definitions_list": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "inward",
            "is_active",
            "is_default",
            "logo_props",
            "name",
            "outward",
            "sort_order",
        ]
    ),
    "work_item_relation_definitions_partial_update": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "inward",
            "is_active",
            "is_default",
            "logo_props",
            "name",
            "outward",
            "sort_order",
        ]
    ),
    "work_item_relation_definitions_retrieve": frozenset(
        [
            "all",
            "color",
            "created_at",
            "created_by_id",
            "description",
            "external_id",
            "external_source",
            "id",
            "inward",
            "is_active",
            "is_default",
            "logo_props",
            "name",
            "outward",
            "sort_order",
        ]
    ),
    "work_item_type_properties_list": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_type_properties_retrieve": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "work_item_types_create": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_destroy": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_enable": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_list": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_mark_default": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_partial_update": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_item_types_retrieve": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "work_items_archive": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_create": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_destroy": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_list": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_partial_update": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_retrieve": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_retrieve_by_identifier": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_unarchive": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_upsert": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "work_items_use": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "custom_fields",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "workflow_states_create": frozenset(
        [
            "all",
            "allow_issue_creation",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "state_id",
            "type",
            "workflow_id",
        ]
    ),
    "workflow_states_destroy": frozenset(
        [
            "all",
            "allow_issue_creation",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "state_id",
            "type",
            "workflow_id",
        ]
    ),
    "workflow_states_list": frozenset(
        [
            "all",
            "allow_issue_creation",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "state_id",
            "type",
            "workflow_id",
        ]
    ),
    "workflow_states_partial_update": frozenset(
        [
            "all",
            "allow_issue_creation",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "state_id",
            "type",
            "workflow_id",
        ]
    ),
    "workflow_states_retrieve": frozenset(
        [
            "all",
            "allow_issue_creation",
            "created_at",
            "created_by_id",
            "id",
            "is_default",
            "state_id",
            "type",
            "workflow_id",
        ]
    ),
    "workflow_transitions_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "id",
            "member_ids",
            "rejection_state_id",
            "required_approvals",
            "transition_state_id",
            "workflow_state_id",
        ]
    ),
    "workflow_transitions_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "id",
            "member_ids",
            "rejection_state_id",
            "required_approvals",
            "transition_state_id",
            "workflow_state_id",
        ]
    ),
    "workflow_transitions_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "id",
            "member_ids",
            "rejection_state_id",
            "required_approvals",
            "transition_state_id",
            "workflow_state_id",
        ]
    ),
    "workflow_transitions_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "id",
            "member_ids",
            "rejection_state_id",
            "required_approvals",
            "transition_state_id",
            "workflow_state_id",
        ]
    ),
    "workflow_transitions_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "id",
            "member_ids",
            "rejection_state_id",
            "required_approvals",
            "transition_state_id",
            "workflow_state_id",
        ]
    ),
    "workflows_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "id",
            "is_active",
            "is_default",
            "name",
            "work_item_type_ids",
        ]
    ),
    "workflows_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "id",
            "is_active",
            "is_default",
            "name",
            "work_item_type_ids",
        ]
    ),
    "workflows_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "id",
            "is_active",
            "is_default",
            "name",
            "work_item_type_ids",
        ]
    ),
    "workflows_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "id",
            "is_active",
            "is_default",
            "name",
            "work_item_type_ids",
        ]
    ),
    "workflows_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "id",
            "is_active",
            "is_default",
            "name",
            "work_item_type_ids",
        ]
    ),
    "worklogs_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "duration",
            "id",
            "logged_by_id",
            "updated_at",
            "work_item_id",
        ]
    ),
    "worklogs_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "duration",
            "id",
            "logged_by_id",
            "updated_at",
            "work_item_id",
        ]
    ),
    "worklogs_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "duration",
            "id",
            "logged_by_id",
            "updated_at",
            "work_item_id",
        ]
    ),
    "worklogs_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "duration",
            "id",
            "logged_by_id",
            "updated_at",
            "work_item_id",
        ]
    ),
    "worklogs_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description",
            "duration",
            "id",
            "logged_by_id",
            "updated_at",
            "work_item_id",
        ]
    ),
    "workspace_automation_activities_list": frozenset(
        [
            "actor_id",
            "all",
            "automation_edge_id",
            "automation_id",
            "automation_node_id",
            "automation_run_id",
            "automation_scope",
            "automation_version_id",
            "created_at",
            "epoch",
            "field",
            "id",
            "new_identifier",
            "new_value",
            "node_execution_id",
            "old_identifier",
            "old_value",
            "verb",
        ]
    ),
    "workspace_automation_activities_retrieve": frozenset(
        [
            "actor_id",
            "all",
            "automation_edge_id",
            "automation_id",
            "automation_node_id",
            "automation_run_id",
            "automation_scope",
            "automation_version_id",
            "created_at",
            "epoch",
            "field",
            "id",
            "new_identifier",
            "new_value",
            "node_execution_id",
            "old_identifier",
            "old_value",
            "verb",
        ]
    ),
    "workspace_automation_edges_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_edges_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_edges_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_edges_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_edges_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "execution_order",
            "id",
            "source_node_id",
            "target_node_id",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_nodes_create": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_nodes_destroy": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_nodes_list": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_nodes_partial_update": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automation_nodes_retrieve": frozenset(
        [
            "all",
            "config",
            "created_at",
            "created_by_id",
            "handler_name",
            "id",
            "is_enabled",
            "last_triggered_at",
            "name",
            "next_scheduled_at",
            "node_type",
            "updated_at",
            "version_id",
        ]
    ),
    "workspace_automations_create": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "workspace_automations_destroy": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "workspace_automations_list": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "workspace_automations_partial_update": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "workspace_automations_retrieve": frozenset(
        [
            "all",
            "bot_user_id",
            "created_at",
            "created_by_id",
            "current_version_id",
            "description",
            "id",
            "is_enabled",
            "is_global",
            "last_run_at",
            "name",
            "project_ids",
            "run_count",
            "scope",
            "status",
            "updated_at",
        ]
    ),
    "workspace_members_list": frozenset(["all", "id", "member_id", "role"]),
    "workspace_pages_create": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "workspace_pages_destroy": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "workspace_pages_list": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "workspace_pages_partial_update": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "workspace_pages_retrieve": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "collection_id",
            "color",
            "created_at",
            "created_by_id",
            "description_html",
            "description_stripped",
            "external_id",
            "external_source",
            "id",
            "is_global",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "parent_id",
            "sort_order",
            "view_props",
        ]
    ),
    "workspace_views_create": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "workspace_views_destroy": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "workspace_views_list": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "workspace_views_partial_update": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "workspace_views_retrieve": frozenset(
        [
            "access",
            "all",
            "archived_at",
            "created_at",
            "created_by_id",
            "description",
            "display_filters",
            "display_properties",
            "filters",
            "id",
            "is_locked",
            "logo_props",
            "name",
            "owned_by_id",
            "pql_filters",
            "query",
            "sort_order",
        ]
    ),
    "workspace_work_item_properties_create": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_properties_destroy": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_properties_list": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_properties_partial_update": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_properties_retrieve": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_templates_create": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "workspace_work_item_templates_destroy": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "workspace_work_item_templates_list": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "workspace_work_item_templates_partial_update": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "workspace_work_item_templates_retrieve": frozenset(
        [
            "all",
            "created_at",
            "created_by_id",
            "description_html",
            "id",
            "is_published",
            "name",
            "short_description",
            "short_id",
            "slug",
            "template_data",
            "template_type",
        ]
    ),
    "workspace_work_item_type_properties_list": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_type_properties_retrieve": frozenset(
        [
            "all",
            "created_at",
            "default_value",
            "description",
            "display_name",
            "external_id",
            "external_source",
            "id",
            "is_active",
            "is_multi",
            "is_required",
            "logo_props",
            "name",
            "options",
            "property_type",
            "relation_type",
            "settings",
            "validation_rules",
        ]
    ),
    "workspace_work_item_types_create": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_item_types_destroy": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_item_types_list": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_item_types_mark_default": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_item_types_partial_update": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_item_types_retrieve": frozenset(
        [
            "all",
            "created_at",
            "description",
            "id",
            "is_active",
            "is_default",
            "is_epic",
            "level",
            "logo_props",
            "name",
        ]
    ),
    "workspace_work_items_list": frozenset(
        [
            "all",
            "archived_at",
            "assignee_ids",
            "created_at",
            "created_by_id",
            "cycle_id",
            "id",
            "identifier",
            "is_draft",
            "label_ids",
            "module_ids",
            "name",
            "parent_id",
            "priority",
            "project_id",
            "sequence_id",
            "start_date",
            "state_id",
            "target_date",
            "type_id",
        ]
    ),
    "workspaces_retrieve": frozenset(
        [
            "all",
            "created_at",
            "id",
            "logo_url",
            "name",
            "organization_size",
            "owner_id",
            "slug",
            "timezone",
            "updated_at",
        ]
    ),
}

ORDER_BY: dict[str, frozenset[str]] = {
    "activities_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "assets_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "attachments_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "audit_logs_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "comments_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "customer_properties_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "customer_requests_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "customers_list": frozenset(["-created_at", "-id", "-name", "created_at", "id", "name"]),
    "cycles_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "estimate_points_list": frozenset(["-created_at", "-id", "-key", "created_at", "id", "key"]),
    "estimates_list": frozenset(["-created_at", "-id", "-name", "created_at", "id", "name"]),
    "group_sync_project_mappings_list": frozenset(
        ["-created_at", "-id", "-idp_group_name", "created_at", "id", "idp_group_name"]
    ),
    "group_sync_workspace_mappings_list": frozenset(
        ["-created_at", "-id", "-idp_group_name", "created_at", "id", "idp_group_name"]
    ),
    "initiative_labels_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "initiatives_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "intakes_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "labels_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "links_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "members_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "milestones_list": frozenset(
        ["-created_at", "-id", "-target_date", "created_at", "id", "target_date"]
    ),
    "modules_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "pages_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "permission_schemes_list": frozenset(
        ["-id", "-name", "-namespace", "-sort_order", "id", "name", "namespace", "sort_order"]
    ),
    "project_automation_activities_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "project_automation_edges_list": frozenset(
        ["-created_at", "-execution_order", "-id", "created_at", "execution_order", "id"]
    ),
    "project_automation_nodes_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "project_automations_list": frozenset(
        ["-created_at", "-id", "-name", "created_at", "id", "name"]
    ),
    "project_members_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "project_pages_list": frozenset(
        ["-created_at", "-id", "-name", "-updated_at", "created_at", "id", "name", "updated_at"]
    ),
    "project_views_list": frozenset(
        [
            "-created_at",
            "-id",
            "-sort_order",
            "-updated_at",
            "created_at",
            "id",
            "sort_order",
            "updated_at",
        ]
    ),
    "project_work_item_templates_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "projects_list": frozenset(["-created_at", "-id", "-name", "created_at", "id", "name"]),
    "release_comments_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "release_labels_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "release_links_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "release_tags_list": frozenset(
        ["-created_at", "-id", "-version", "created_at", "id", "version"]
    ),
    "releases_list": frozenset(
        [
            "-created_at",
            "-id",
            "-name",
            "-release_date",
            "-target_date",
            "created_at",
            "id",
            "name",
            "release_date",
            "target_date",
        ]
    ),
    "roles_list": frozenset(
        ["-id", "-level", "-name", "-namespace", "id", "level", "name", "namespace"]
    ),
    "states_list": frozenset(["-created_at", "-id", "-sequence", "created_at", "id", "sequence"]),
    "stickies_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "teamspaces_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "user_assets_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "webhook_logs_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "webhooks_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "work_item_properties_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "work_item_property_contexts_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "work_item_property_options_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "work_item_type_properties_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "work_item_types_list": frozenset(
        ["-created_at", "-id", "-level", "-name", "created_at", "id", "level", "name"]
    ),
    "work_items_list": frozenset(
        [
            "-created_at",
            "-id",
            "-priority",
            "-sequence_id",
            "-sort_order",
            "-state_group",
            "-updated_at",
            "created_at",
            "id",
            "priority",
            "sequence_id",
            "sort_order",
            "state_group",
            "updated_at",
        ]
    ),
    "workflow_states_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workflow_transitions_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workflows_list": frozenset(["-created_at", "-id", "-name", "created_at", "id", "name"]),
    "worklogs_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workspace_automation_activities_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workspace_automation_edges_list": frozenset(
        ["-created_at", "-execution_order", "-id", "created_at", "execution_order", "id"]
    ),
    "workspace_automation_nodes_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workspace_automations_list": frozenset(
        ["-created_at", "-id", "-name", "created_at", "id", "name"]
    ),
    "workspace_members_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workspace_pages_list": frozenset(
        ["-created_at", "-id", "-name", "-updated_at", "created_at", "id", "name", "updated_at"]
    ),
    "workspace_views_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "workspace_work_item_properties_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "workspace_work_item_property_options_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "workspace_work_item_templates_list": frozenset(["-created_at", "-id", "created_at", "id"]),
    "workspace_work_item_type_properties_list": frozenset(
        ["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
    ),
    "workspace_work_item_types_list": frozenset(
        ["-created_at", "-id", "-level", "-name", "created_at", "id", "level", "name"]
    ),
    "workspace_work_items_list": frozenset(
        [
            "-created_at",
            "-id",
            "-priority",
            "-sequence_id",
            "-sort_order",
            "-state_group",
            "-updated_at",
            "created_at",
            "id",
            "priority",
            "sequence_id",
            "sort_order",
            "state_group",
            "updated_at",
        ]
    ),
}

EXPAND: dict[str, frozenset[str]] = {
    "activities_list": frozenset(["actor"]),
    "activities_retrieve": frozenset(["actor"]),
    "collections_members_list": frozenset(["member"]),
    "comments_create": frozenset(["actor"]),
    "comments_destroy": frozenset(["actor"]),
    "comments_list": frozenset(["actor"]),
    "comments_partial_update": frozenset(["actor"]),
    "comments_retrieve": frozenset(["actor"]),
    "cycles_create": frozenset(["owned_by"]),
    "cycles_destroy": frozenset(["owned_by"]),
    "cycles_list": frozenset(["owned_by"]),
    "cycles_partial_update": frozenset(["owned_by"]),
    "cycles_retrieve": frozenset(["owned_by"]),
    "cycles_upsert": frozenset(["owned_by"]),
    "estimates_create": frozenset(["points"]),
    "estimates_destroy": frozenset(["points"]),
    "estimates_list": frozenset(["points"]),
    "estimates_partial_update": frozenset(["points"]),
    "estimates_retrieve": frozenset(["points"]),
    "estimates_upsert": frozenset(["points"]),
    "initiatives_create": frozenset(["lead"]),
    "initiatives_destroy": frozenset(["lead"]),
    "initiatives_list": frozenset(["lead"]),
    "initiatives_partial_update": frozenset(["lead"]),
    "initiatives_retrieve": frozenset(["lead"]),
    "modules_create": frozenset(["lead", "members"]),
    "modules_destroy": frozenset(["lead", "members"]),
    "modules_list": frozenset(["lead", "members"]),
    "modules_partial_update": frozenset(["lead", "members"]),
    "modules_retrieve": frozenset(["lead", "members"]),
    "modules_upsert": frozenset(["lead", "members"]),
    "pages_create": frozenset(["owned_by"]),
    "pages_destroy": frozenset(["owned_by"]),
    "pages_list": frozenset(["owned_by"]),
    "pages_partial_update": frozenset(["owned_by"]),
    "pages_retrieve": frozenset(["owned_by"]),
    "project_members_create": frozenset(["member"]),
    "project_members_destroy": frozenset(["member"]),
    "project_members_list": frozenset(["member"]),
    "project_members_partial_update": frozenset(["member"]),
    "project_members_retrieve": frozenset(["member"]),
    "project_pages_create": frozenset(["owned_by", "parent"]),
    "project_pages_destroy": frozenset(["owned_by", "parent"]),
    "project_pages_list": frozenset(["owned_by", "parent"]),
    "project_pages_partial_update": frozenset(["owned_by", "parent"]),
    "project_pages_retrieve": frozenset(["owned_by", "parent"]),
    "project_views_create": frozenset(["owned_by"]),
    "project_views_destroy": frozenset(["owned_by"]),
    "project_views_list": frozenset(["owned_by"]),
    "project_views_partial_update": frozenset(["owned_by"]),
    "project_views_retrieve": frozenset(["owned_by"]),
    "projects_create": frozenset(["default_assignee", "project_lead"]),
    "projects_destroy": frozenset(["default_assignee", "project_lead"]),
    "projects_list": frozenset(["default_assignee", "project_lead"]),
    "projects_partial_update": frozenset(["default_assignee", "project_lead"]),
    "projects_retrieve": frozenset(["default_assignee", "project_lead"]),
    "projects_upsert": frozenset(["default_assignee", "project_lead"]),
    "releases_create": frozenset(["lead", "tag"]),
    "releases_destroy": frozenset(["lead", "tag"]),
    "releases_list": frozenset(["lead", "tag"]),
    "releases_partial_update": frozenset(["lead", "tag"]),
    "releases_retrieve": frozenset(["lead", "tag"]),
    "teamspaces_create": frozenset(["lead"]),
    "teamspaces_destroy": frozenset(["lead"]),
    "teamspaces_list": frozenset(["lead"]),
    "teamspaces_partial_update": frozenset(["lead"]),
    "teamspaces_retrieve": frozenset(["lead"]),
    "work_item_comments_upsert": frozenset(["actor"]),
    "work_items_archive": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_create": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_destroy": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_list": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_partial_update": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_retrieve": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_retrieve_by_identifier": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_unarchive": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_upsert": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "work_items_use": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
    "worklogs_create": frozenset(["logged_by"]),
    "worklogs_destroy": frozenset(["logged_by"]),
    "worklogs_list": frozenset(["logged_by"]),
    "worklogs_partial_update": frozenset(["logged_by"]),
    "worklogs_retrieve": frozenset(["logged_by"]),
    "workspace_members_list": frozenset(["member"]),
    "workspace_pages_create": frozenset(["owned_by", "parent"]),
    "workspace_pages_destroy": frozenset(["owned_by", "parent"]),
    "workspace_pages_list": frozenset(["owned_by", "parent"]),
    "workspace_pages_partial_update": frozenset(["owned_by", "parent"]),
    "workspace_pages_retrieve": frozenset(["owned_by", "parent"]),
    "workspace_views_create": frozenset(["owned_by"]),
    "workspace_views_destroy": frozenset(["owned_by"]),
    "workspace_views_list": frozenset(["owned_by"]),
    "workspace_views_partial_update": frozenset(["owned_by"]),
    "workspace_views_retrieve": frozenset(["owned_by"]),
    "workspace_work_items_list": frozenset(
        ["assignees", "cycle", "labels", "modules", "parent", "state", "type"]
    ),
}

PAGINATION: dict[str, frozenset[str]] = {
    "activities_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "assets_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "attachments_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "audit_logs_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "comments_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "customer_properties_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "customer_requests_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "customers_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "cycles_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "estimate_points_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "estimates_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "group_sync_project_mappings_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "group_sync_workspace_mappings_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "initiative_labels_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "initiatives_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "intakes_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "labels_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "links_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "members_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "milestones_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "modules_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "pages_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "permission_schemes_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_automation_activities_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_automation_edges_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_automation_nodes_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_automations_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_members_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_pages_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_views_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "project_work_item_templates_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "projects_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "release_comments_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "release_labels_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "release_links_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "release_tags_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "releases_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "roles_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "states_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "stickies_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "teamspaces_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "user_assets_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "webhook_logs_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "webhooks_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_item_properties_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_item_property_contexts_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_item_property_options_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_item_relation_definitions_list": frozenset(["count", "offset", "per_page"]),
    "work_item_type_properties_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_item_types_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "work_items_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workflow_states_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workflow_transitions_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workflows_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "worklogs_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_automation_activities_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_automation_edges_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_automation_nodes_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_automations_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_members_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_pages_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_views_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_work_item_properties_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_work_item_property_options_list": frozenset(
        ["count", "offset", "paginate", "per_page"]
    ),
    "workspace_work_item_templates_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_work_item_type_properties_list": frozenset(
        ["count", "offset", "paginate", "per_page"]
    ),
    "workspace_work_item_types_list": frozenset(["count", "offset", "paginate", "per_page"]),
    "workspace_work_items_list": frozenset(["count", "offset", "paginate", "per_page"]),
}

ERROR_CODES: frozenset[str] = frozenset(
    [
        "batch_failed",
        "conflict",
        "count_pagination_disabled",
        "forbidden",
        "governance_migration_in_progress",
        "invalid_request",
        "listing_authorization_misconfigured",
        "method_not_allowed",
        "not_acceptable",
        "not_found",
        "ordering_not_cursor_eligible",
        "payload_too_large",
        "payment_required",
        "rate_limited",
        "server_error",
        "service_unavailable",
        "states_managed_at_workspace",
        "unauthorized",
        "unsupported_media_type",
        "work_item_types_managed_at_project",
        "work_item_types_managed_at_workspace",
        "workflow_transition_denied",
    ]
)

ActivitiesListField = Literal[
    "actor_id",
    "all",
    "comment",
    "created_at",
    "duration",
    "epoch",
    "external_id",
    "external_source",
    "field",
    "id",
    "issue_comment_id",
    "new_identifier_id",
    "new_value",
    "old_identifier_id",
    "old_value",
    "verb",
    "work_item_id",
]
ActivitiesRetrieveField = Literal[
    "actor_id",
    "all",
    "comment",
    "created_at",
    "duration",
    "epoch",
    "external_id",
    "external_source",
    "field",
    "id",
    "issue_comment_id",
    "new_identifier_id",
    "new_value",
    "old_identifier_id",
    "old_value",
    "verb",
    "work_item_id",
]
AssetsCreateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
]
AssetsDestroyField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
]
AssetsListField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
]
AssetsPartialUpdateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
]
AssetsRetrieveField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
]
AttachmentsCreateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
    "work_item_id",
]
AttachmentsDestroyField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
    "work_item_id",
]
AttachmentsListField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
    "work_item_id",
]
AttachmentsPartialUpdateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
    "work_item_id",
]
AttachmentsRetrieveField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "is_uploaded",
    "name",
    "size",
    "work_item_id",
]
AuditLogsListField = Literal[
    "actor_display_name",
    "actor_email",
    "actor_id",
    "actor_type",
    "all",
    "category",
    "created_at",
    "event_id",
    "event_name",
    "id",
    "ip_address",
    "metadata",
    "new_value",
    "old_value",
    "outcome",
    "project_id",
    "reason",
    "sequence_number",
    "source",
    "target_display_name",
    "target_id",
    "target_type",
    "user_agent",
    "workspace_id",
]
AuditLogsRetrieveField = Literal[
    "actor_display_name",
    "actor_email",
    "actor_id",
    "actor_type",
    "all",
    "category",
    "created_at",
    "event_id",
    "event_name",
    "id",
    "ip_address",
    "metadata",
    "new_value",
    "old_value",
    "outcome",
    "project_id",
    "reason",
    "sequence_number",
    "source",
    "target_display_name",
    "target_id",
    "target_type",
    "user_agent",
    "workspace_id",
]
CollectionsMembersListField = Literal[
    "access", "all", "collection_id", "created_at", "created_by_id", "id", "member_id", "source"
]
CollectionsPagesSearchField = Literal["all", "id", "logo_props", "name"]
CommentsCreateField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
CommentsDestroyField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
CommentsListField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
CommentsPartialUpdateField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
CommentsRetrieveField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
CustomerPropertiesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "sort_order",
    "validation_rules",
]
CustomerPropertiesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "sort_order",
    "validation_rules",
]
CustomerPropertiesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "sort_order",
    "validation_rules",
]
CustomerPropertiesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "sort_order",
    "validation_rules",
]
CustomerPropertiesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "sort_order",
    "validation_rules",
]
CustomerRequestsCreateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "customer_id",
    "description",
    "description_html",
    "id",
    "link",
    "name",
]
CustomerRequestsDestroyField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "customer_id",
    "description",
    "description_html",
    "id",
    "link",
    "name",
]
CustomerRequestsListField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "customer_id",
    "description",
    "description_html",
    "id",
    "link",
    "name",
]
CustomerRequestsPartialUpdateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "customer_id",
    "description",
    "description_html",
    "id",
    "link",
    "name",
]
CustomerRequestsRetrieveField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "customer_id",
    "description",
    "description_html",
    "id",
    "link",
    "name",
]
CustomersCreateField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CustomersDestroyField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CustomersListField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CustomersPartialUpdateField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CustomersRetrieveField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CustomersUpsertField = Literal[
    "all",
    "archived_at",
    "contract_status",
    "created_at",
    "created_by_id",
    "customer_request_count",
    "description",
    "description_html",
    "domain",
    "email",
    "employees",
    "external_id",
    "external_source",
    "id",
    "logo_asset_id",
    "logo_props",
    "logo_url",
    "name",
    "revenue",
    "stage",
    "website_url",
]
CyclesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
CyclesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
CyclesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
CyclesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
CyclesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
CyclesUpsertField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "end_date",
    "external_id",
    "external_source",
    "id",
    "logo_props",
    "name",
    "owned_by_id",
    "sort_order",
    "start_date",
    "timezone",
]
EstimatePointsCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatePointsDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatePointsListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatePointsPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatePointsRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatePointsUpsertField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "estimate_id",
    "external_id",
    "external_source",
    "id",
    "key",
    "value",
]
EstimatesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
EstimatesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
EstimatesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
EstimatesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
EstimatesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
EstimatesUpsertField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "last_used",
    "name",
    "type",
]
GroupSyncProjectMappingsCreateField = Literal[
    "all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"
]
GroupSyncProjectMappingsDestroyField = Literal[
    "all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"
]
GroupSyncProjectMappingsListField = Literal[
    "all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"
]
GroupSyncProjectMappingsRetrieveField = Literal[
    "all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"
]
GroupSyncProjectMappingsUpdateField = Literal[
    "all", "all_projects", "created_at", "id", "idp_group_name", "project_id", "role_slug"
]
GroupSyncWorkspaceMappingsCreateField = Literal[
    "all", "created_at", "id", "idp_group_name", "role_slug"
]
GroupSyncWorkspaceMappingsDestroyField = Literal[
    "all", "created_at", "id", "idp_group_name", "role_slug"
]
GroupSyncWorkspaceMappingsListField = Literal[
    "all", "created_at", "id", "idp_group_name", "role_slug"
]
GroupSyncWorkspaceMappingsRetrieveField = Literal[
    "all", "created_at", "id", "idp_group_name", "role_slug"
]
GroupSyncWorkspaceMappingsUpdateField = Literal[
    "all", "created_at", "id", "idp_group_name", "role_slug"
]
InitiativeLabelsCreateField = Literal[
    "all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"
]
InitiativeLabelsDestroyField = Literal[
    "all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"
]
InitiativeLabelsListField = Literal[
    "all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"
]
InitiativeLabelsPartialUpdateField = Literal[
    "all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"
]
InitiativeLabelsRetrieveField = Literal[
    "all", "color", "created_at", "created_by_id", "description", "id", "name", "sort_order"
]
InitiativesCreateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "description_html",
    "end_date",
    "id",
    "label_ids",
    "lead_id",
    "logo_props",
    "name",
    "project_ids",
    "start_date",
    "state",
]
InitiativesDestroyField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "description_html",
    "end_date",
    "id",
    "label_ids",
    "lead_id",
    "logo_props",
    "name",
    "project_ids",
    "start_date",
    "state",
]
InitiativesListField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "description_html",
    "end_date",
    "id",
    "label_ids",
    "lead_id",
    "logo_props",
    "name",
    "project_ids",
    "start_date",
    "state",
]
InitiativesPartialUpdateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "description_html",
    "end_date",
    "id",
    "label_ids",
    "lead_id",
    "logo_props",
    "name",
    "project_ids",
    "start_date",
    "state",
]
InitiativesRetrieveField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "description_html",
    "end_date",
    "id",
    "label_ids",
    "lead_id",
    "logo_props",
    "name",
    "project_ids",
    "start_date",
    "state",
]
IntakesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "duplicate_to_id",
    "external_id",
    "external_source",
    "id",
    "intake_id",
    "name",
    "priority",
    "snoozed_till",
    "source",
    "source_email",
    "state_id",
    "status",
    "work_item_id",
]
IntakesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "duplicate_to_id",
    "external_id",
    "external_source",
    "id",
    "intake_id",
    "name",
    "priority",
    "snoozed_till",
    "source",
    "source_email",
    "state_id",
    "status",
    "work_item_id",
]
IntakesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "duplicate_to_id",
    "external_id",
    "external_source",
    "id",
    "intake_id",
    "name",
    "priority",
    "snoozed_till",
    "source",
    "source_email",
    "state_id",
    "status",
    "work_item_id",
]
IntakesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "duplicate_to_id",
    "external_id",
    "external_source",
    "id",
    "intake_id",
    "name",
    "priority",
    "snoozed_till",
    "source",
    "source_email",
    "state_id",
    "status",
    "work_item_id",
]
IntakesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "duplicate_to_id",
    "external_id",
    "external_source",
    "id",
    "intake_id",
    "name",
    "priority",
    "snoozed_till",
    "source",
    "source_email",
    "state_id",
    "status",
    "work_item_id",
]
LabelsCreateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LabelsDestroyField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LabelsListField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LabelsPartialUpdateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LabelsRetrieveField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LabelsUpsertField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "name",
    "parent_id",
    "sort_order",
]
LinksCreateField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"
]
LinksDestroyField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"
]
LinksListField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"
]
LinksPartialUpdateField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"
]
LinksRetrieveField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "title", "url", "work_item_id"
]
MembersBulkField = Literal[
    "accepted",
    "all",
    "created_at",
    "created_by_id",
    "email",
    "id",
    "message",
    "responded_at",
    "role",
]
MembersCreateField = Literal[
    "accepted",
    "all",
    "created_at",
    "created_by_id",
    "email",
    "id",
    "message",
    "responded_at",
    "role",
]
MembersDestroyField = Literal[
    "accepted",
    "all",
    "created_at",
    "created_by_id",
    "email",
    "id",
    "message",
    "responded_at",
    "role",
]
MembersListField = Literal[
    "accepted",
    "all",
    "created_at",
    "created_by_id",
    "email",
    "id",
    "message",
    "responded_at",
    "role",
]
MembersRetrieveField = Literal[
    "accepted",
    "all",
    "created_at",
    "created_by_id",
    "email",
    "id",
    "message",
    "responded_at",
    "role",
]
MilestonesCreateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
MilestonesDestroyField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
MilestonesListField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
MilestonesPartialUpdateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
MilestonesRetrieveField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
MilestonesUpsertField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "external_id",
    "external_source",
    "id",
    "target_date",
    "title",
]
ModulesCreateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
ModulesDestroyField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
ModulesListField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
ModulesPartialUpdateField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
ModulesRetrieveField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
ModulesUpsertField = Literal[
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "sort_order",
    "start_date",
    "status",
    "target_date",
]
PagesCreateField = Literal[
    "access",
    "all",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "is_global",
    "logo_props",
    "name",
    "owned_by_id",
    "page_ids",
    "sort_order",
]
PagesDestroyField = Literal[
    "access",
    "all",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "is_global",
    "logo_props",
    "name",
    "owned_by_id",
    "page_ids",
    "sort_order",
]
PagesListField = Literal[
    "access",
    "all",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "is_global",
    "logo_props",
    "name",
    "owned_by_id",
    "page_ids",
    "sort_order",
]
PagesPartialUpdateField = Literal[
    "access",
    "all",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "is_global",
    "logo_props",
    "name",
    "owned_by_id",
    "page_ids",
    "sort_order",
]
PagesRetrieveField = Literal[
    "access",
    "all",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "is_global",
    "logo_props",
    "name",
    "owned_by_id",
    "page_ids",
    "sort_order",
]
PermissionSchemesListField = Literal[
    "all",
    "description",
    "id",
    "is_system",
    "name",
    "namespace",
    "permissions",
    "slug",
    "sort_order",
]
PermissionSchemesRetrieveField = Literal[
    "all",
    "description",
    "id",
    "is_system",
    "name",
    "namespace",
    "permissions",
    "slug",
    "sort_order",
]
ProjectAutomationActivitiesListField = Literal[
    "actor_id",
    "all",
    "automation_edge_id",
    "automation_id",
    "automation_node_id",
    "automation_run_id",
    "automation_scope",
    "automation_version_id",
    "created_at",
    "epoch",
    "field",
    "id",
    "new_identifier",
    "new_value",
    "node_execution_id",
    "old_identifier",
    "old_value",
    "verb",
]
ProjectAutomationActivitiesRetrieveField = Literal[
    "actor_id",
    "all",
    "automation_edge_id",
    "automation_id",
    "automation_node_id",
    "automation_run_id",
    "automation_scope",
    "automation_version_id",
    "created_at",
    "epoch",
    "field",
    "id",
    "new_identifier",
    "new_value",
    "node_execution_id",
    "old_identifier",
    "old_value",
    "verb",
]
ProjectAutomationEdgesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
ProjectAutomationEdgesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
ProjectAutomationEdgesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
ProjectAutomationEdgesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
ProjectAutomationEdgesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
ProjectAutomationNodesCreateField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
ProjectAutomationNodesDestroyField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
ProjectAutomationNodesListField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
ProjectAutomationNodesPartialUpdateField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
ProjectAutomationNodesRetrieveField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
ProjectAutomationsCreateField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
ProjectAutomationsDestroyField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
ProjectAutomationsListField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
ProjectAutomationsPartialUpdateField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
ProjectAutomationsRetrieveField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
ProjectMembersCreateField = Literal["all", "id", "member_id", "role"]
ProjectMembersDestroyField = Literal["all", "id", "member_id", "role"]
ProjectMembersListField = Literal["all", "id", "member_id", "role"]
ProjectMembersPartialUpdateField = Literal["all", "id", "member_id", "role"]
ProjectMembersRetrieveField = Literal["all", "id", "member_id", "role"]
ProjectPagesCreateField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
ProjectPagesDestroyField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
ProjectPagesListField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
ProjectPagesPartialUpdateField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
ProjectPagesRetrieveField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
ProjectViewsCreateField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
ProjectViewsDestroyField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
ProjectViewsListField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
ProjectViewsPartialUpdateField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
ProjectViewsRetrieveField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
ProjectWorkItemTemplatesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
ProjectWorkItemTemplatesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
ProjectWorkItemTemplatesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
ProjectWorkItemTemplatesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
ProjectWorkItemTemplatesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
ProjectsCreateField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ProjectsDestroyField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ProjectsListField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ProjectsPartialUpdateField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ProjectsRetrieveField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ProjectsUpsertField = Literal[
    "all",
    "archive_in",
    "archived_at",
    "close_in",
    "cover_image",
    "cover_image_url",
    "created_at",
    "created_by_id",
    "cycle_view",
    "default_assignee_id",
    "default_state_id",
    "description",
    "emoji",
    "estimate_id",
    "external_id",
    "external_source",
    "guest_view_all_features",
    "icon_prop",
    "id",
    "identifier",
    "intake_view",
    "is_issue_type_enabled",
    "is_time_tracking_enabled",
    "issue_views_view",
    "logo_props",
    "module_view",
    "name",
    "network",
    "page_view",
    "priority",
    "project_lead_id",
    "start_date",
    "state_id",
    "target_date",
    "timezone",
]
ReleaseCommentsCreateField = Literal[
    "all",
    "comment_html",
    "comment_id",
    "created_at",
    "created_by_id",
    "edited_at",
    "id",
    "is_hidden",
    "is_resolved",
    "parent_id",
    "release_id",
]
ReleaseCommentsDestroyField = Literal[
    "all",
    "comment_html",
    "comment_id",
    "created_at",
    "created_by_id",
    "edited_at",
    "id",
    "is_hidden",
    "is_resolved",
    "parent_id",
    "release_id",
]
ReleaseCommentsListField = Literal[
    "all",
    "comment_html",
    "comment_id",
    "created_at",
    "created_by_id",
    "edited_at",
    "id",
    "is_hidden",
    "is_resolved",
    "parent_id",
    "release_id",
]
ReleaseCommentsPartialUpdateField = Literal[
    "all",
    "comment_html",
    "comment_id",
    "created_at",
    "created_by_id",
    "edited_at",
    "id",
    "is_hidden",
    "is_resolved",
    "parent_id",
    "release_id",
]
ReleaseCommentsRetrieveField = Literal[
    "all",
    "comment_html",
    "comment_id",
    "created_at",
    "created_by_id",
    "edited_at",
    "id",
    "is_hidden",
    "is_resolved",
    "parent_id",
    "release_id",
]
ReleaseLabelsCreateField = Literal[
    "all", "color", "created_at", "created_by_id", "id", "name", "sort_order"
]
ReleaseLabelsDestroyField = Literal[
    "all", "color", "created_at", "created_by_id", "id", "name", "sort_order"
]
ReleaseLabelsListField = Literal[
    "all", "color", "created_at", "created_by_id", "id", "name", "sort_order"
]
ReleaseLabelsPartialUpdateField = Literal[
    "all", "color", "created_at", "created_by_id", "id", "name", "sort_order"
]
ReleaseLabelsRetrieveField = Literal[
    "all", "color", "created_at", "created_by_id", "id", "name", "sort_order"
]
ReleaseLinksCreateField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"
]
ReleaseLinksDestroyField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"
]
ReleaseLinksListField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"
]
ReleaseLinksPartialUpdateField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"
]
ReleaseLinksRetrieveField = Literal[
    "all", "created_at", "created_by_id", "id", "metadata", "release_id", "title", "url"
]
ReleaseTagsCreateField = Literal[
    "all", "commit_hash", "created_at", "created_by_id", "description", "git_tag", "id", "version"
]
ReleaseTagsDestroyField = Literal[
    "all", "commit_hash", "created_at", "created_by_id", "description", "git_tag", "id", "version"
]
ReleaseTagsListField = Literal[
    "all", "commit_hash", "created_at", "created_by_id", "description", "git_tag", "id", "version"
]
ReleaseTagsPartialUpdateField = Literal[
    "all", "commit_hash", "created_at", "created_by_id", "description", "git_tag", "id", "version"
]
ReleaseTagsRetrieveField = Literal[
    "all", "commit_hash", "created_at", "created_by_id", "description", "git_tag", "id", "version"
]
ReleasesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "description_id",
    "external_id",
    "external_source",
    "id",
    "is_latest",
    "is_prerelease",
    "label_ids",
    "lead_id",
    "name",
    "release_date",
    "status",
    "tag_id",
    "target_date",
]
ReleasesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "description_id",
    "external_id",
    "external_source",
    "id",
    "is_latest",
    "is_prerelease",
    "label_ids",
    "lead_id",
    "name",
    "release_date",
    "status",
    "tag_id",
    "target_date",
]
ReleasesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "description_id",
    "external_id",
    "external_source",
    "id",
    "is_latest",
    "is_prerelease",
    "label_ids",
    "lead_id",
    "name",
    "release_date",
    "status",
    "tag_id",
    "target_date",
]
ReleasesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "description_id",
    "external_id",
    "external_source",
    "id",
    "is_latest",
    "is_prerelease",
    "label_ids",
    "lead_id",
    "name",
    "release_date",
    "status",
    "tag_id",
    "target_date",
]
ReleasesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "description_id",
    "external_id",
    "external_source",
    "id",
    "is_latest",
    "is_prerelease",
    "label_ids",
    "lead_id",
    "name",
    "release_date",
    "status",
    "tag_id",
    "target_date",
]
RolesListField = Literal[
    "all", "description", "id", "is_system", "level", "name", "namespace", "slug", "status"
]
RolesRetrieveField = Literal[
    "all", "description", "id", "is_system", "level", "name", "namespace", "slug", "status"
]
StatesCreateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StatesDestroyField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StatesListField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StatesPartialUpdateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StatesRetrieveField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StatesUpsertField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "group",
    "id",
    "is_default",
    "is_triage",
    "name",
    "sequence",
]
StickiesCreateField = Literal[
    "all",
    "background_color",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "id",
    "logo_props",
    "name",
    "owner_id",
    "sort_order",
]
StickiesDestroyField = Literal[
    "all",
    "background_color",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "id",
    "logo_props",
    "name",
    "owner_id",
    "sort_order",
]
StickiesListField = Literal[
    "all",
    "background_color",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "id",
    "logo_props",
    "name",
    "owner_id",
    "sort_order",
]
StickiesPartialUpdateField = Literal[
    "all",
    "background_color",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "id",
    "logo_props",
    "name",
    "owner_id",
    "sort_order",
]
StickiesRetrieveField = Literal[
    "all",
    "background_color",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "id",
    "logo_props",
    "name",
    "owner_id",
    "sort_order",
]
TeamspacesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "project_ids",
]
TeamspacesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "project_ids",
]
TeamspacesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "project_ids",
]
TeamspacesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "project_ids",
]
TeamspacesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "lead_id",
    "logo_props",
    "member_ids",
    "name",
    "project_ids",
]
UserAssetsCreateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "id",
    "is_uploaded",
    "name",
    "size",
    "user_id",
]
UserAssetsDestroyField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "id",
    "is_uploaded",
    "name",
    "size",
    "user_id",
]
UserAssetsListField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "id",
    "is_uploaded",
    "name",
    "size",
    "user_id",
]
UserAssetsPartialUpdateField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "id",
    "is_uploaded",
    "name",
    "size",
    "user_id",
]
UserAssetsRetrieveField = Literal[
    "all",
    "asset_url",
    "attributes",
    "content_type",
    "created_at",
    "created_by_id",
    "entity_type",
    "id",
    "is_uploaded",
    "name",
    "size",
    "user_id",
]
WebhookLogsListField = Literal[
    "all",
    "created_at",
    "duration_ms",
    "error_message",
    "event_type",
    "id",
    "request_body",
    "request_headers",
    "request_method",
    "response_body",
    "response_headers",
    "response_status",
    "retry_count",
    "status_text",
    "webhook_id",
]
WebhookLogsRetrieveField = Literal[
    "all",
    "created_at",
    "duration_ms",
    "error_message",
    "event_type",
    "id",
    "request_body",
    "request_headers",
    "request_method",
    "response_body",
    "response_headers",
    "response_status",
    "retry_count",
    "status_text",
    "webhook_id",
]
WebhooksCreateField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "url",
    "version",
]
WebhooksDestroyField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "url",
    "version",
]
WebhooksListField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "url",
    "version",
]
WebhooksPartialUpdateField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "url",
    "version",
]
WebhooksRegenerateField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "secret_key",
    "url",
    "version",
]
WebhooksRetrieveField = Literal[
    "all",
    "content_type",
    "created_at",
    "created_by_id",
    "id",
    "is_active",
    "name",
    "scopes",
    "url",
    "version",
]
WorkItemCommentsUpsertField = Literal[
    "access",
    "actor_id",
    "all",
    "comment_html",
    "comment_stripped",
    "created_at",
    "created_by_id",
    "edited_at",
    "external_id",
    "external_source",
    "id",
    "work_item_id",
]
WorkItemPropertiesCreateField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemPropertiesDestroyField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemPropertiesListField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemPropertiesPartialUpdateField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemPropertiesRetrieveField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemPropertyContextsCreateField = Literal[
    "all",
    "applies_to_all_projects",
    "applies_to_all_work_item_types",
    "created_at",
    "default_value",
    "external_id",
    "external_source",
    "id",
    "is_default",
    "is_multi",
    "is_required",
    "issue_type_ids",
    "name",
    "options",
    "project_ids",
    "settings",
    "sort_order",
]
WorkItemPropertyContextsDestroyField = Literal[
    "all",
    "applies_to_all_projects",
    "applies_to_all_work_item_types",
    "created_at",
    "default_value",
    "external_id",
    "external_source",
    "id",
    "is_default",
    "is_multi",
    "is_required",
    "issue_type_ids",
    "name",
    "options",
    "project_ids",
    "settings",
    "sort_order",
]
WorkItemPropertyContextsListField = Literal[
    "all",
    "applies_to_all_projects",
    "applies_to_all_work_item_types",
    "created_at",
    "default_value",
    "external_id",
    "external_source",
    "id",
    "is_default",
    "is_multi",
    "is_required",
    "issue_type_ids",
    "name",
    "options",
    "project_ids",
    "settings",
    "sort_order",
]
WorkItemPropertyContextsPartialUpdateField = Literal[
    "all",
    "applies_to_all_projects",
    "applies_to_all_work_item_types",
    "created_at",
    "default_value",
    "external_id",
    "external_source",
    "id",
    "is_default",
    "is_multi",
    "is_required",
    "issue_type_ids",
    "name",
    "options",
    "project_ids",
    "settings",
    "sort_order",
]
WorkItemPropertyContextsRetrieveField = Literal[
    "all",
    "applies_to_all_projects",
    "applies_to_all_work_item_types",
    "created_at",
    "default_value",
    "external_id",
    "external_source",
    "id",
    "is_default",
    "is_multi",
    "is_required",
    "issue_type_ids",
    "name",
    "options",
    "project_ids",
    "settings",
    "sort_order",
]
WorkItemRelationDefinitionsCreateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "inward",
    "is_active",
    "is_default",
    "logo_props",
    "name",
    "outward",
    "sort_order",
]
WorkItemRelationDefinitionsDestroyField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "inward",
    "is_active",
    "is_default",
    "logo_props",
    "name",
    "outward",
    "sort_order",
]
WorkItemRelationDefinitionsListField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "inward",
    "is_active",
    "is_default",
    "logo_props",
    "name",
    "outward",
    "sort_order",
]
WorkItemRelationDefinitionsPartialUpdateField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "inward",
    "is_active",
    "is_default",
    "logo_props",
    "name",
    "outward",
    "sort_order",
]
WorkItemRelationDefinitionsRetrieveField = Literal[
    "all",
    "color",
    "created_at",
    "created_by_id",
    "description",
    "external_id",
    "external_source",
    "id",
    "inward",
    "is_active",
    "is_default",
    "logo_props",
    "name",
    "outward",
    "sort_order",
]
WorkItemTypePropertiesListField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemTypePropertiesRetrieveField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkItemTypesCreateField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesDestroyField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesEnableField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesListField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesMarkDefaultField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesPartialUpdateField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemTypesRetrieveField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkItemsArchiveField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsCreateField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsDestroyField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsListField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsPartialUpdateField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsRetrieveField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsRetrieveByIdentifierField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsUnarchiveField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsUpsertField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkItemsUseField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "custom_fields",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkflowStatesCreateField = Literal[
    "all",
    "allow_issue_creation",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "state_id",
    "type",
    "workflow_id",
]
WorkflowStatesDestroyField = Literal[
    "all",
    "allow_issue_creation",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "state_id",
    "type",
    "workflow_id",
]
WorkflowStatesListField = Literal[
    "all",
    "allow_issue_creation",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "state_id",
    "type",
    "workflow_id",
]
WorkflowStatesPartialUpdateField = Literal[
    "all",
    "allow_issue_creation",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "state_id",
    "type",
    "workflow_id",
]
WorkflowStatesRetrieveField = Literal[
    "all",
    "allow_issue_creation",
    "created_at",
    "created_by_id",
    "id",
    "is_default",
    "state_id",
    "type",
    "workflow_id",
]
WorkflowTransitionsCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "id",
    "member_ids",
    "rejection_state_id",
    "required_approvals",
    "transition_state_id",
    "workflow_state_id",
]
WorkflowTransitionsDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "id",
    "member_ids",
    "rejection_state_id",
    "required_approvals",
    "transition_state_id",
    "workflow_state_id",
]
WorkflowTransitionsListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "id",
    "member_ids",
    "rejection_state_id",
    "required_approvals",
    "transition_state_id",
    "workflow_state_id",
]
WorkflowTransitionsPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "id",
    "member_ids",
    "rejection_state_id",
    "required_approvals",
    "transition_state_id",
    "workflow_state_id",
]
WorkflowTransitionsRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "id",
    "member_ids",
    "rejection_state_id",
    "required_approvals",
    "transition_state_id",
    "workflow_state_id",
]
WorkflowsCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "id",
    "is_active",
    "is_default",
    "name",
    "work_item_type_ids",
]
WorkflowsDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "id",
    "is_active",
    "is_default",
    "name",
    "work_item_type_ids",
]
WorkflowsListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "id",
    "is_active",
    "is_default",
    "name",
    "work_item_type_ids",
]
WorkflowsPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "id",
    "is_active",
    "is_default",
    "name",
    "work_item_type_ids",
]
WorkflowsRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "id",
    "is_active",
    "is_default",
    "name",
    "work_item_type_ids",
]
WorklogsCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "duration",
    "id",
    "logged_by_id",
    "updated_at",
    "work_item_id",
]
WorklogsDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "duration",
    "id",
    "logged_by_id",
    "updated_at",
    "work_item_id",
]
WorklogsListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "duration",
    "id",
    "logged_by_id",
    "updated_at",
    "work_item_id",
]
WorklogsPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "duration",
    "id",
    "logged_by_id",
    "updated_at",
    "work_item_id",
]
WorklogsRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description",
    "duration",
    "id",
    "logged_by_id",
    "updated_at",
    "work_item_id",
]
WorkspaceAutomationActivitiesListField = Literal[
    "actor_id",
    "all",
    "automation_edge_id",
    "automation_id",
    "automation_node_id",
    "automation_run_id",
    "automation_scope",
    "automation_version_id",
    "created_at",
    "epoch",
    "field",
    "id",
    "new_identifier",
    "new_value",
    "node_execution_id",
    "old_identifier",
    "old_value",
    "verb",
]
WorkspaceAutomationActivitiesRetrieveField = Literal[
    "actor_id",
    "all",
    "automation_edge_id",
    "automation_id",
    "automation_node_id",
    "automation_run_id",
    "automation_scope",
    "automation_version_id",
    "created_at",
    "epoch",
    "field",
    "id",
    "new_identifier",
    "new_value",
    "node_execution_id",
    "old_identifier",
    "old_value",
    "verb",
]
WorkspaceAutomationEdgesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
WorkspaceAutomationEdgesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
WorkspaceAutomationEdgesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
WorkspaceAutomationEdgesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
WorkspaceAutomationEdgesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "execution_order",
    "id",
    "source_node_id",
    "target_node_id",
    "updated_at",
    "version_id",
]
WorkspaceAutomationNodesCreateField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
WorkspaceAutomationNodesDestroyField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
WorkspaceAutomationNodesListField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
WorkspaceAutomationNodesPartialUpdateField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
WorkspaceAutomationNodesRetrieveField = Literal[
    "all",
    "config",
    "created_at",
    "created_by_id",
    "handler_name",
    "id",
    "is_enabled",
    "last_triggered_at",
    "name",
    "next_scheduled_at",
    "node_type",
    "updated_at",
    "version_id",
]
WorkspaceAutomationsCreateField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
WorkspaceAutomationsDestroyField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
WorkspaceAutomationsListField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
WorkspaceAutomationsPartialUpdateField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
WorkspaceAutomationsRetrieveField = Literal[
    "all",
    "bot_user_id",
    "created_at",
    "created_by_id",
    "current_version_id",
    "description",
    "id",
    "is_enabled",
    "is_global",
    "last_run_at",
    "name",
    "project_ids",
    "run_count",
    "scope",
    "status",
    "updated_at",
]
WorkspaceMembersListField = Literal["all", "id", "member_id", "role"]
WorkspacePagesCreateField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
WorkspacePagesDestroyField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
WorkspacePagesListField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
WorkspacePagesPartialUpdateField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
WorkspacePagesRetrieveField = Literal[
    "access",
    "all",
    "archived_at",
    "collection_id",
    "color",
    "created_at",
    "created_by_id",
    "description_html",
    "description_stripped",
    "external_id",
    "external_source",
    "id",
    "is_global",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "parent_id",
    "sort_order",
    "view_props",
]
WorkspaceViewsCreateField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
WorkspaceViewsDestroyField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
WorkspaceViewsListField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
WorkspaceViewsPartialUpdateField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
WorkspaceViewsRetrieveField = Literal[
    "access",
    "all",
    "archived_at",
    "created_at",
    "created_by_id",
    "description",
    "display_filters",
    "display_properties",
    "filters",
    "id",
    "is_locked",
    "logo_props",
    "name",
    "owned_by_id",
    "pql_filters",
    "query",
    "sort_order",
]
WorkspaceWorkItemPropertiesCreateField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemPropertiesDestroyField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemPropertiesListField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemPropertiesPartialUpdateField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemPropertiesRetrieveField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemTemplatesCreateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
WorkspaceWorkItemTemplatesDestroyField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
WorkspaceWorkItemTemplatesListField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
WorkspaceWorkItemTemplatesPartialUpdateField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
WorkspaceWorkItemTemplatesRetrieveField = Literal[
    "all",
    "created_at",
    "created_by_id",
    "description_html",
    "id",
    "is_published",
    "name",
    "short_description",
    "short_id",
    "slug",
    "template_data",
    "template_type",
]
WorkspaceWorkItemTypePropertiesListField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemTypePropertiesRetrieveField = Literal[
    "all",
    "created_at",
    "default_value",
    "description",
    "display_name",
    "external_id",
    "external_source",
    "id",
    "is_active",
    "is_multi",
    "is_required",
    "logo_props",
    "name",
    "options",
    "property_type",
    "relation_type",
    "settings",
    "validation_rules",
]
WorkspaceWorkItemTypesCreateField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemTypesDestroyField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemTypesListField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemTypesMarkDefaultField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemTypesPartialUpdateField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemTypesRetrieveField = Literal[
    "all",
    "created_at",
    "description",
    "id",
    "is_active",
    "is_default",
    "is_epic",
    "level",
    "logo_props",
    "name",
]
WorkspaceWorkItemsListField = Literal[
    "all",
    "archived_at",
    "assignee_ids",
    "created_at",
    "created_by_id",
    "cycle_id",
    "id",
    "identifier",
    "is_draft",
    "label_ids",
    "module_ids",
    "name",
    "parent_id",
    "priority",
    "project_id",
    "sequence_id",
    "start_date",
    "state_id",
    "target_date",
    "type_id",
]
WorkspacesRetrieveField = Literal[
    "all",
    "created_at",
    "id",
    "logo_url",
    "name",
    "organization_size",
    "owner_id",
    "slug",
    "timezone",
    "updated_at",
]
ActivitiesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
AssetsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
AttachmentsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
AuditLogsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
CommentsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
CustomerPropertiesListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
CustomerRequestsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
CustomersListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
CyclesListOrderBy = Literal["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
EstimatePointsListOrderBy = Literal["-created_at", "-id", "-key", "created_at", "id", "key"]
EstimatesListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
GroupSyncProjectMappingsListOrderBy = Literal[
    "-created_at", "-id", "-idp_group_name", "created_at", "id", "idp_group_name"
]
GroupSyncWorkspaceMappingsListOrderBy = Literal[
    "-created_at", "-id", "-idp_group_name", "created_at", "id", "idp_group_name"
]
InitiativeLabelsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
InitiativesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
IntakesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
LabelsListOrderBy = Literal["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
LinksListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
MembersListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
MilestonesListOrderBy = Literal[
    "-created_at", "-id", "-target_date", "created_at", "id", "target_date"
]
ModulesListOrderBy = Literal["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
PagesListOrderBy = Literal["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
PermissionSchemesListOrderBy = Literal[
    "-id", "-name", "-namespace", "-sort_order", "id", "name", "namespace", "sort_order"
]
ProjectAutomationActivitiesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ProjectAutomationEdgesListOrderBy = Literal[
    "-created_at", "-execution_order", "-id", "created_at", "execution_order", "id"
]
ProjectAutomationNodesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ProjectAutomationsListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
ProjectMembersListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ProjectPagesListOrderBy = Literal[
    "-created_at", "-id", "-name", "-updated_at", "created_at", "id", "name", "updated_at"
]
ProjectViewsListOrderBy = Literal[
    "-created_at",
    "-id",
    "-sort_order",
    "-updated_at",
    "created_at",
    "id",
    "sort_order",
    "updated_at",
]
ProjectWorkItemTemplatesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ProjectsListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
ReleaseCommentsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ReleaseLabelsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
ReleaseLinksListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
ReleaseTagsListOrderBy = Literal["-created_at", "-id", "-version", "created_at", "id", "version"]
ReleasesListOrderBy = Literal[
    "-created_at",
    "-id",
    "-name",
    "-release_date",
    "-target_date",
    "created_at",
    "id",
    "name",
    "release_date",
    "target_date",
]
RolesListOrderBy = Literal[
    "-id", "-level", "-name", "-namespace", "id", "level", "name", "namespace"
]
StatesListOrderBy = Literal["-created_at", "-id", "-sequence", "created_at", "id", "sequence"]
StickiesListOrderBy = Literal["-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"]
TeamspacesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
UserAssetsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WebhookLogsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WebhooksListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkItemPropertiesListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkItemPropertyContextsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkItemPropertyOptionsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkItemTypePropertiesListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkItemTypesListOrderBy = Literal[
    "-created_at", "-id", "-level", "-name", "created_at", "id", "level", "name"
]
WorkItemsListOrderBy = Literal[
    "-created_at",
    "-id",
    "-priority",
    "-sequence_id",
    "-sort_order",
    "-state_group",
    "-updated_at",
    "created_at",
    "id",
    "priority",
    "sequence_id",
    "sort_order",
    "state_group",
    "updated_at",
]
WorkflowStatesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkflowTransitionsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkflowsListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
WorklogsListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkspaceAutomationActivitiesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkspaceAutomationEdgesListOrderBy = Literal[
    "-created_at", "-execution_order", "-id", "created_at", "execution_order", "id"
]
WorkspaceAutomationNodesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkspaceAutomationsListOrderBy = Literal["-created_at", "-id", "-name", "created_at", "id", "name"]
WorkspaceMembersListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkspacePagesListOrderBy = Literal[
    "-created_at", "-id", "-name", "-updated_at", "created_at", "id", "name", "updated_at"
]
WorkspaceViewsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkspaceWorkItemPropertiesListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkspaceWorkItemPropertyOptionsListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkspaceWorkItemTemplatesListOrderBy = Literal["-created_at", "-id", "created_at", "id"]
WorkspaceWorkItemTypePropertiesListOrderBy = Literal[
    "-created_at", "-id", "-sort_order", "created_at", "id", "sort_order"
]
WorkspaceWorkItemTypesListOrderBy = Literal[
    "-created_at", "-id", "-level", "-name", "created_at", "id", "level", "name"
]
WorkspaceWorkItemsListOrderBy = Literal[
    "-created_at",
    "-id",
    "-priority",
    "-sequence_id",
    "-sort_order",
    "-state_group",
    "-updated_at",
    "created_at",
    "id",
    "priority",
    "sequence_id",
    "sort_order",
    "state_group",
    "updated_at",
]


class ActivitiesListFilters(TypedDict, total=False):
    actor_id: str
    created_at__gte: str
    created_at__lte: str
    field: str
    search: str
    verb: str


class AttachmentsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    is_uploaded: bool


class AuditLogsListFilters(TypedDict, total=False):
    actor_id: str
    category: str
    created_after: str
    created_before: str
    event_name: str
    ip_address: str
    outcome: str
    project_id: str
    search: str
    target_id: str
    target_type: str


class CommentsListFilters(TypedDict, total=False):
    access: str
    external_id: str
    external_source: str
    search: str


class CustomerPropertiesListFilters(TypedDict, total=False):
    display_name: str
    is_active: bool
    is_required: bool
    name: str
    property_type: str
    search: str


class CustomerRequestsListFilters(TypedDict, total=False):
    search: str


class CustomersListFilters(TypedDict, total=False):
    contract_status: str
    domain: str
    external_id: str
    external_source: str
    name: str
    search: str
    stage: str


class CyclesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    owned_by_id: str
    search: str


class EstimatePointsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    key: int
    search: str
    value: str


class EstimatesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str
    type: str
    type__in: Sequence[str]


class GroupSyncProjectMappingsListFilters(TypedDict, total=False):
    search: str


class GroupSyncWorkspaceMappingsListFilters(TypedDict, total=False):
    search: str


class InitiativeLabelsListFilters(TypedDict, total=False):
    name: str
    search: str


class InitiativesListFilters(TypedDict, total=False):
    lead_id: str
    name: str
    search: str
    state: str
    state__in: Sequence[str]


class IntakesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    search: str
    source: str
    status: int
    status__in: Sequence[int]
    work_item_id: str


class LabelsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    parent_id: str
    parent_id__isnull: bool
    search: str


class LinksListFilters(TypedDict, total=False):
    search: str
    title: str
    url: str


class MembersListFilters(TypedDict, total=False):
    accepted: bool
    email: str
    search: str


class MilestonesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str
    target_date: str
    target_date__gte: str
    target_date__lte: str


class ModulesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    lead_id: str
    name: str
    search: str
    status: str
    status__in: Sequence[str]


class PagesListFilters(TypedDict, total=False):
    access: int
    is_default: bool
    is_global: bool
    owned_by_id: str
    search: str


class PermissionSchemesListFilters(TypedDict, total=False):
    search: str


class ProjectAutomationActivitiesListFilters(TypedDict, total=False):
    created_at__gt: str
    field: str
    verb: str


class ProjectAutomationEdgesListFilters(TypedDict, total=False):
    source_node_id: str
    target_node_id: str


class ProjectAutomationNodesListFilters(TypedDict, total=False):
    handler_name: str
    is_enabled: bool
    name: str
    node_type: str
    search: str


class ProjectAutomationsListFilters(TypedDict, total=False):
    is_enabled: bool
    is_global: bool
    name: str
    scope: str
    search: str
    status: str


class ProjectMembersListFilters(TypedDict, total=False):
    member_id: str
    member_id__in: Sequence[str]
    role: str
    role__in: Sequence[str]
    search: str


class ProjectPagesListFilters(TypedDict, total=False):
    access: int
    collection_id: str
    external_id: str
    external_source: str
    is_global: bool
    is_locked: bool
    owned_by_id: str
    parent_id: str
    search: str
    type: str


class ProjectViewsListFilters(TypedDict, total=False):
    access: int
    is_locked: bool
    name: str
    owned_by_id: str
    search: str


class ProjectWorkItemTemplatesListFilters(TypedDict, total=False):
    is_published: bool
    search: str
    short_id: str


class ProjectsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    identifier: str
    include_archived: bool
    is_archived: bool
    key: str
    name: str
    network: int
    priority: str
    priority__in: Sequence[str]
    search: str


class ProjectsSummaryFilters(TypedDict, total=False):
    counts: str


class ReleaseCommentsListFilters(TypedDict, total=False):
    is_resolved: bool
    parent_id: str
    search: str


class ReleaseLabelsListFilters(TypedDict, total=False):
    name: str
    search: str


class ReleaseLinksListFilters(TypedDict, total=False):
    search: str


class ReleaseTagsListFilters(TypedDict, total=False):
    search: str
    version: str


class ReleasesListFilters(TypedDict, total=False):
    is_latest: bool
    is_prerelease: bool
    lead_id: str
    name: str
    release_date: str
    search: str
    status: str
    status__in: Sequence[str]
    tag_id: str
    target_date: str


class RolesListFilters(TypedDict, total=False):
    is_system: bool
    namespace: str
    search: str
    slug: str


class StatesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    group: str
    group__in: Sequence[str]
    is_default: bool
    name: str
    search: str


class StickiesListFilters(TypedDict, total=False):
    color: str
    owner_id: str
    search: str


class TeamspacesListFilters(TypedDict, total=False):
    lead_id: str
    name: str
    search: str


class WebhooksListFilters(TypedDict, total=False):
    is_active: bool
    name: str
    search: str
    url: str


class WorkItemPropertiesListFilters(TypedDict, total=False):
    display_name: str
    external_id: str
    external_source: str
    name: str
    search: str


class WorkItemPropertyContextsListFilters(TypedDict, total=False):
    name: str
    search: str


class WorkItemPropertyOptionsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str


class WorkItemTypesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str


class WorkItemTypesSchemaFilters(TypedDict, total=False):
    include: str


class WorkItemsListFilters(TypedDict, total=False):
    assignee_id: str
    assignee_id__in: Sequence[str]
    assignee_id__isnull: bool
    created_at__gte: str
    created_at__lte: str
    cycle_id: str
    cycle_id__in: Sequence[str]
    cycle_id__isnull: bool
    external_id: str
    external_source: str
    is_draft: bool
    label_id: str
    label_id__in: Sequence[str]
    label_id__isnull: bool
    module_id: str
    module_id__in: Sequence[str]
    module_id__isnull: bool
    parent_id: str
    parent_id__in: Sequence[str]
    parent_id__isnull: bool
    priority: str
    priority__in: Sequence[str]
    project_id: str
    project_id__in: Sequence[str]
    search: str
    sequence_id: int
    start_date__gte: str
    start_date__lte: str
    state_group: str
    state_group__in: Sequence[str]
    state_id: str
    state_id__in: Sequence[str]
    target_date__gte: str
    target_date__lte: str
    type_id: str
    type_id__in: Sequence[str]
    updated_at__gte: str
    updated_at__lte: str


class WorkflowsListFilters(TypedDict, total=False):
    search: str


class WorklogsListFilters(TypedDict, total=False):
    duration__gte: int
    duration__lte: int
    logged_by_id: str
    search: str


class WorkspaceAutomationActivitiesListFilters(TypedDict, total=False):
    created_at__gt: str
    field: str
    verb: str


class WorkspaceAutomationEdgesListFilters(TypedDict, total=False):
    source_node_id: str
    target_node_id: str


class WorkspaceAutomationNodesListFilters(TypedDict, total=False):
    handler_name: str
    is_enabled: bool
    name: str
    node_type: str
    search: str


class WorkspaceAutomationsListFilters(TypedDict, total=False):
    is_enabled: bool
    is_global: bool
    name: str
    scope: str
    search: str
    status: str


class WorkspaceMembersListFilters(TypedDict, total=False):
    member_id: str
    member_id__in: Sequence[str]
    role: str
    role__in: Sequence[str]
    search: str


class WorkspacePagesListFilters(TypedDict, total=False):
    access: int
    collection_id: str
    external_id: str
    external_source: str
    is_global: bool
    is_locked: bool
    owned_by_id: str
    parent_id: str
    search: str
    type: str


class WorkspaceViewsListFilters(TypedDict, total=False):
    access: int
    is_locked: bool
    name: str
    owned_by_id: str
    search: str


class WorkspaceWorkItemPropertiesListFilters(TypedDict, total=False):
    display_name: str
    external_id: str
    external_source: str
    name: str
    search: str


class WorkspaceWorkItemPropertyOptionsListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str


class WorkspaceWorkItemTemplatesListFilters(TypedDict, total=False):
    is_published: bool
    search: str
    short_id: str


class WorkspaceWorkItemTypesListFilters(TypedDict, total=False):
    external_id: str
    external_source: str
    name: str
    search: str


class WorkspaceWorkItemsListFilters(TypedDict, total=False):
    assignee_id: str
    assignee_id__in: Sequence[str]
    assignee_id__isnull: bool
    created_at__gte: str
    created_at__lte: str
    cycle_id: str
    cycle_id__in: Sequence[str]
    cycle_id__isnull: bool
    external_id: str
    external_source: str
    is_draft: bool
    label_id: str
    label_id__in: Sequence[str]
    label_id__isnull: bool
    module_id: str
    module_id__in: Sequence[str]
    module_id__isnull: bool
    parent_id: str
    parent_id__in: Sequence[str]
    parent_id__isnull: bool
    priority: str
    priority__in: Sequence[str]
    project_id: str
    project_id__in: Sequence[str]
    search: str
    sequence_id: int
    start_date__gte: str
    start_date__lte: str
    state_group: str
    state_group__in: Sequence[str]
    state_id: str
    state_id__in: Sequence[str]
    target_date__gte: str
    target_date__lte: str
    type_id: str
    type_id__in: Sequence[str]
    updated_at__gte: str
    updated_at__lte: str
