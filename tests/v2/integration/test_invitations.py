"""Workspace invitations against a real server; `create`/`bulk` send real
invitation emails, so this suite uses throwaway `+`-tagged addresses and
deletes every invite it creates. Not verified against a live server yet."""

from __future__ import annotations

import uuid

import pytest

from plane.api.v2.invitations import Invitations
from plane.client import PlaneClient
from plane.models.v2.invitations import BulkCreateWorkspaceInvites, CreateWorkspaceInvite


def _throwaway_email(prefix: str) -> str:
    return f"sdk-it-{prefix}-{uuid.uuid4().hex[:8]}@example.invalid"


@pytest.fixture(scope="module")
def invitations(client: PlaneClient) -> Invitations:
    return client.v2.workspaces.invitations


def test_list(invitations: Invitations, workspace_slug: str) -> None:
    page = invitations.list(workspace_slug)
    assert isinstance(page.data, list)


def test_create_retrieve_delete(invitations: Invitations, workspace_slug: str) -> None:
    email = _throwaway_email("single")
    created = invitations.create(workspace_slug, CreateWorkspaceInvite(email=email))
    try:
        fetched = invitations.retrieve(workspace_slug, created.id)
        assert fetched.email == email
        assert fetched.accepted is False
    finally:
        invitations.delete(workspace_slug, created.id)


def test_bulk_creates_every_new_email(invitations: Invitations, workspace_slug: str) -> None:
    emails = [_throwaway_email("bulk-a"), _throwaway_email("bulk-b")]
    created = invitations.bulk(workspace_slug, BulkCreateWorkspaceInvites(emails=emails))
    try:
        assert {row.email for row in created} == set(emails)
    finally:
        for row in created:
            try:
                invitations.delete(workspace_slug, row.id)
            except Exception:
                pass


def test_bulk_skips_already_invited_emails(invitations: Invitations, workspace_slug: str) -> None:
    """Re-inviting an already-pending email is a silent no-op server-side (see
    `WorkspaceInviteViewSet.bulk`'s `existing` set) -- confirms the SDK surfaces
    that as an empty result, not an error."""
    email = _throwaway_email("dedup")
    first = invitations.create(workspace_slug, CreateWorkspaceInvite(email=email))
    try:
        second = invitations.bulk(workspace_slug, BulkCreateWorkspaceInvites(emails=[email]))
        assert second == []
    finally:
        invitations.delete(workspace_slug, first.id)
