"""Offline contract tests for the v1 /relations/ response used by Plane CE."""

import pytest
import responses
from pydantic import ValidationError

from plane.api.work_items.relations import WorkItemRelations
from plane.config import Configuration
from plane.errors.errors import HttpError
from plane.models.work_items import WorkItemRelationResponse

GROUPS = (
    "blocking",
    "blocked_by",
    "duplicate",
    "relates_to",
    "start_after",
    "start_before",
    "finish_after",
    "finish_before",
)
BASE = "https://plane.example.com"
URL = f"{BASE}/api/v1/workspaces/acme/projects/source-project/work-items/source-item/relations/"
TARGET = {"project_id": "other-project", "issue_id": "related-item"}


@pytest.fixture
def relations() -> WorkItemRelations:
    return WorkItemRelations(Configuration(base_path=BASE, api_key="test-key"))


@pytest.mark.parametrize("group", GROUPS)
@responses.activate
def test_list_preserves_related_item_and_project(relations: WorkItemRelations, group: str) -> None:
    # CE's IssueRelationListCreateAPIEndpoint returns references, not bare IDs.
    payload = {key: [TARGET] if key == group else [] for key in GROUPS}
    responses.get(URL, json=payload)

    result = relations.list("acme", "source-project", "source-item")

    target = getattr(result, group)[0]
    assert target.issue_id == "related-item"
    assert target.project_id == "other-project"
    assert result.model_dump() == payload
    assert len(responses.calls) == 1


@responses.activate
def test_list_empty_groups(relations: WorkItemRelations) -> None:
    payload = {key: [] for key in GROUPS}
    responses.get(URL, json=payload)

    result = relations.list("acme", "source-project", "source-item")

    assert result.model_dump() == payload


def test_bare_ids_remain_supported() -> None:
    payload = {key: ["related-item"] for key in GROUPS}

    result = WorkItemRelationResponse.model_validate(payload)

    assert result.model_dump() == payload
    assert result.blocking == ["related-item"]


def test_reference_preserves_additional_response_fields() -> None:
    payload = {key: [] for key in GROUPS}
    payload["blocking"] = [{**TARGET, "identifier": "OTHER-42"}]

    result = WorkItemRelationResponse.model_validate(payload)

    assert result.model_dump() == payload


@pytest.mark.parametrize("target", [{"project_id": "p"}, {"issue_id": "i"}, 42, None])
def test_malformed_reference_is_rejected(target: object) -> None:
    payload = {key: [] for key in GROUPS}
    payload["blocking"] = [target]

    with pytest.raises(ValidationError):
        WorkItemRelationResponse.model_validate(payload)


@pytest.mark.parametrize("status", [401, 403, 404, 500])
@responses.activate
def test_http_errors_are_not_empty_relations(relations: WorkItemRelations, status: int) -> None:
    responses.get(URL, status=status, json={"error": "Request failed."})

    with pytest.raises(HttpError) as error:
        relations.list("acme", "source-project", "source-item")

    assert error.value.status_code == status
