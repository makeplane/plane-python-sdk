"""The path-id naming rule, enforced rather than left to be inferred.

Every path id a v2 method takes is named after the resource it identifies, singular,
with no `_id` suffix -- `slug`, `project`, `work_item`, `state`, `label`, `page`,
`comment`, `release`. The rule matters mechanically, not just cosmetically: `Owned`
matches a child method's leading parameter names against the parent's `_id_names`
exactly, so two exemplars disagreeing about it would leave ~85 follow-on migrations
guessing. The URL *templates* keep the golden's own keys (`{project_id}`,
`{work_item_id}`), and so do model field names; this is about parameters only.

See the "path ids" rule in CLAUDE.md.
"""

import inspect

import pytest

from plane.api.v2.features import WorkspaceFeatures
from plane.api.v2.labels import Labels
from plane.api.v2.pages import ProjectPages, WikiPages
from plane.api.v2.projects import Projects
from plane.api.v2.releases.labels import ReleaseLabels
from plane.api.v2.states import States
from plane.api.v2.work_items import WorkItems
from plane.api.v2.work_items.comments import WorkItemComments
from plane.api.v2.workspaces import Workspaces

MIGRATED = [
    Projects,
    States,
    Labels,
    WorkItems,
    WorkItemComments,
    ReleaseLabels,
    ProjectPages,
    WikiPages,
    Workspaces,
    WorkspaceFeatures,
]


@pytest.mark.parametrize("resource", MIGRATED, ids=lambda cls: cls.__name__)
def test_no_public_method_names_a_path_id_with_an_id_suffix(resource: type) -> None:
    offenders = []
    for name, function in vars(resource).items():
        if name.startswith("_") or not inspect.isfunction(function):
            continue
        offenders += [
            f"{resource.__name__}.{name}({parameter})"
            for parameter in inspect.signature(function).parameters
            if parameter.endswith("_id")
        ]

    assert offenders == [], (
        "path ids are named after the resource they identify, with no `_id` suffix: " f"{offenders}"
    )


def test_a_childs_leading_parameters_match_what_its_parent_binds() -> None:
    """The rule's whole point: `Owned` compares these names literally, so the parent's
    `loaded_names` and the child's leading parameters have to agree."""
    for parent, children in [
        (Projects, [States, Labels, WorkItems]),
        (WorkItems, [WorkItemComments]),
    ]:
        bound = parent.loaded_names
        for child in children:
            leading = tuple(inspect.signature(child.list).parameters)[1 : 1 + len(bound)]
            assert leading == bound, (parent.__name__, child.__name__, leading, bound)
