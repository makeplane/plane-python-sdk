"""A fetched project row that is also the place its children live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.projects import Project
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..automations import ProjectAutomations
    from ..cycles import Cycles
    from ..estimates import Estimates
    from ..features import ProjectFeatures
    from ..intakes import Intakes
    from ..labels import Labels
    from ..members import ProjectMembers
    from ..milestones import Milestones
    from ..modules import Modules
    from ..pages import ProjectPages
    from ..permissions import ProjectPermissions
    from ..projects import Projects
    from ..states import States
    from ..views.project import ProjectViews
    from ..work_item_properties import WorkItemProperties
    from ..work_item_templates.project import ProjectWorkItemTemplates
    from ..work_item_types import WorkItemTypes
    from ..work_items import WorkItems
    from ..workflows import Workflows
    from ..worklogs import ProjectWorklogs

    # Typed views on `Owned`: the child resource's own methods with `slug` and
    # `project` already supplied. One line per method, `bind2` because two path ids
    # are bound. Evaluated only by a type checker -- at runtime these properties
    # return a plain `Owned`.
    #
    # There is one view per resource `Projects.__init__` attaches, and
    # `tests/v2/test_loaded_navigation.py` sweeps that correspondence rather than
    # trusting it: a child attached without a property here fails by name.

    class _OwnedStates(Owned["States"]):
        list = staticmethod(bind2(States.list))
        iterate = staticmethod(bind2(States.iterate))
        retrieve = staticmethod(bind2(States.retrieve))
        find_by_name = staticmethod(bind2(States.find_by_name))
        create = staticmethod(bind2(States.create))
        update = staticmethod(bind2(States.update))
        delete = staticmethod(bind2(States.delete))
        upsert = staticmethod(bind2(States.upsert))
        bulk_create = staticmethod(bind2(States.bulk_create))
        bulk_update = staticmethod(bind2(States.bulk_update))
        bulk_delete = staticmethod(bind2(States.bulk_delete))

    class _OwnedLabels(Owned["Labels"]):
        list = staticmethod(bind2(Labels.list))
        iterate = staticmethod(bind2(Labels.iterate))
        retrieve = staticmethod(bind2(Labels.retrieve))
        find_by_name = staticmethod(bind2(Labels.find_by_name))
        create = staticmethod(bind2(Labels.create))
        update = staticmethod(bind2(Labels.update))
        delete = staticmethod(bind2(Labels.delete))
        upsert = staticmethod(bind2(Labels.upsert))
        bulk_create = staticmethod(bind2(Labels.bulk_create))
        bulk_update = staticmethod(bind2(Labels.bulk_update))
        bulk_delete = staticmethod(bind2(Labels.bulk_delete))

    class _OwnedWorkItems(Owned["WorkItems"]):
        list = staticmethod(bind2(WorkItems.list))
        iterate = staticmethod(bind2(WorkItems.iterate))
        retrieve = staticmethod(bind2(WorkItems.retrieve))
        create = staticmethod(bind2(WorkItems.create))
        update = staticmethod(bind2(WorkItems.update))
        delete = staticmethod(bind2(WorkItems.delete))
        upsert = staticmethod(bind2(WorkItems.upsert))
        archive = staticmethod(bind2(WorkItems.archive))
        unarchive = staticmethod(bind2(WorkItems.unarchive))
        bulk_create = staticmethod(bind2(WorkItems.bulk_create))
        bulk_update = staticmethod(bind2(WorkItems.bulk_update))
        bulk_delete = staticmethod(bind2(WorkItems.bulk_delete))

    class _OwnedCycles(Owned["Cycles"]):
        list = staticmethod(bind2(Cycles.list))
        iterate = staticmethod(bind2(Cycles.iterate))
        retrieve = staticmethod(bind2(Cycles.retrieve))
        find_by_name = staticmethod(bind2(Cycles.find_by_name))
        create = staticmethod(bind2(Cycles.create))
        update = staticmethod(bind2(Cycles.update))
        delete = staticmethod(bind2(Cycles.delete))
        upsert = staticmethod(bind2(Cycles.upsert))
        transfer = staticmethod(bind2(Cycles.transfer))
        bulk_create = staticmethod(bind2(Cycles.bulk_create))
        bulk_update = staticmethod(bind2(Cycles.bulk_update))
        bulk_delete = staticmethod(bind2(Cycles.bulk_delete))

    class _OwnedMilestones(Owned["Milestones"]):
        list = staticmethod(bind2(Milestones.list))
        iterate = staticmethod(bind2(Milestones.iterate))
        retrieve = staticmethod(bind2(Milestones.retrieve))
        find_by_name = staticmethod(bind2(Milestones.find_by_name))
        create = staticmethod(bind2(Milestones.create))
        update = staticmethod(bind2(Milestones.update))
        delete = staticmethod(bind2(Milestones.delete))
        upsert = staticmethod(bind2(Milestones.upsert))
        bulk_create = staticmethod(bind2(Milestones.bulk_create))
        bulk_update = staticmethod(bind2(Milestones.bulk_update))
        bulk_delete = staticmethod(bind2(Milestones.bulk_delete))

    class _OwnedModules(Owned["Modules"]):
        list = staticmethod(bind2(Modules.list))
        iterate = staticmethod(bind2(Modules.iterate))
        retrieve = staticmethod(bind2(Modules.retrieve))
        find_by_name = staticmethod(bind2(Modules.find_by_name))
        create = staticmethod(bind2(Modules.create))
        update = staticmethod(bind2(Modules.update))
        delete = staticmethod(bind2(Modules.delete))
        upsert = staticmethod(bind2(Modules.upsert))
        bulk_create = staticmethod(bind2(Modules.bulk_create))
        bulk_update = staticmethod(bind2(Modules.bulk_update))
        bulk_delete = staticmethod(bind2(Modules.bulk_delete))

    class _OwnedEstimates(Owned["Estimates"]):
        list = staticmethod(bind2(Estimates.list))
        iterate = staticmethod(bind2(Estimates.iterate))
        retrieve = staticmethod(bind2(Estimates.retrieve))
        find_by_name = staticmethod(bind2(Estimates.find_by_name))
        create = staticmethod(bind2(Estimates.create))
        update = staticmethod(bind2(Estimates.update))
        delete = staticmethod(bind2(Estimates.delete))
        upsert = staticmethod(bind2(Estimates.upsert))
        bulk_create = staticmethod(bind2(Estimates.bulk_create))
        bulk_update = staticmethod(bind2(Estimates.bulk_update))
        bulk_delete = staticmethod(bind2(Estimates.bulk_delete))

    class _OwnedIntakes(Owned["Intakes"]):
        list = staticmethod(bind2(Intakes.list))
        iterate = staticmethod(bind2(Intakes.iterate))
        retrieve = staticmethod(bind2(Intakes.retrieve))
        create = staticmethod(bind2(Intakes.create))
        update = staticmethod(bind2(Intakes.update))
        delete = staticmethod(bind2(Intakes.delete))

    class _OwnedProjectMembers(Owned["ProjectMembers"]):
        list = staticmethod(bind2(ProjectMembers.list))
        iterate = staticmethod(bind2(ProjectMembers.iterate))
        retrieve = staticmethod(bind2(ProjectMembers.retrieve))
        create = staticmethod(bind2(ProjectMembers.create))
        update = staticmethod(bind2(ProjectMembers.update))
        delete = staticmethod(bind2(ProjectMembers.delete))

    class _OwnedProjectViews(Owned["ProjectViews"]):
        list = staticmethod(bind2(ProjectViews.list))
        iterate = staticmethod(bind2(ProjectViews.iterate))
        retrieve = staticmethod(bind2(ProjectViews.retrieve))
        create = staticmethod(bind2(ProjectViews.create))
        update = staticmethod(bind2(ProjectViews.update))
        delete = staticmethod(bind2(ProjectViews.delete))

    class _OwnedProjectFeatures(Owned["ProjectFeatures"]):
        retrieve = staticmethod(bind2(ProjectFeatures.retrieve))
        update = staticmethod(bind2(ProjectFeatures.update))

    class _OwnedProjectPermissions(Owned["ProjectPermissions"]):
        me = staticmethod(bind2(ProjectPermissions.me))

    class _OwnedProjectWorkItemTemplates(Owned["ProjectWorkItemTemplates"]):
        list = staticmethod(bind2(ProjectWorkItemTemplates.list))
        iterate = staticmethod(bind2(ProjectWorkItemTemplates.iterate))
        retrieve = staticmethod(bind2(ProjectWorkItemTemplates.retrieve))
        create = staticmethod(bind2(ProjectWorkItemTemplates.create))
        update = staticmethod(bind2(ProjectWorkItemTemplates.update))
        delete = staticmethod(bind2(ProjectWorkItemTemplates.delete))
        use = staticmethod(bind2(ProjectWorkItemTemplates.use))

    class _OwnedProjectWorklogs(Owned["ProjectWorklogs"]):
        summary = staticmethod(bind2(ProjectWorklogs.summary))

    class _OwnedProjectPages(Owned["ProjectPages"]):
        list = staticmethod(bind2(ProjectPages.list))
        iterate = staticmethod(bind2(ProjectPages.iterate))
        retrieve = staticmethod(bind2(ProjectPages.retrieve))
        find_by_name = staticmethod(bind2(ProjectPages.find_by_name))
        create = staticmethod(bind2(ProjectPages.create))
        update = staticmethod(bind2(ProjectPages.update))
        delete = staticmethod(bind2(ProjectPages.delete))

    class _OwnedProjectAutomations(Owned["ProjectAutomations"]):
        list = staticmethod(bind2(ProjectAutomations.list))
        iterate = staticmethod(bind2(ProjectAutomations.iterate))
        retrieve = staticmethod(bind2(ProjectAutomations.retrieve))
        find_by_name = staticmethod(bind2(ProjectAutomations.find_by_name))
        create = staticmethod(bind2(ProjectAutomations.create))
        update = staticmethod(bind2(ProjectAutomations.update))
        delete = staticmethod(bind2(ProjectAutomations.delete))
        set_status = staticmethod(bind2(ProjectAutomations.set_status))

    class _OwnedWorkItemTypes(Owned["WorkItemTypes"]):
        list = staticmethod(bind2(WorkItemTypes.list))
        iterate = staticmethod(bind2(WorkItemTypes.iterate))
        retrieve = staticmethod(bind2(WorkItemTypes.retrieve))
        find_by_name = staticmethod(bind2(WorkItemTypes.find_by_name))
        create = staticmethod(bind2(WorkItemTypes.create))
        update = staticmethod(bind2(WorkItemTypes.update))
        delete = staticmethod(bind2(WorkItemTypes.delete))
        enable = staticmethod(bind2(WorkItemTypes.enable))
        import_types = staticmethod(bind2(WorkItemTypes.import_types))
        mark_default = staticmethod(bind2(WorkItemTypes.mark_default))
        schema = staticmethod(bind2(WorkItemTypes.schema))

    class _OwnedWorkItemProperties(Owned["WorkItemProperties"]):
        list = staticmethod(bind2(WorkItemProperties.list))
        iterate = staticmethod(bind2(WorkItemProperties.iterate))
        retrieve = staticmethod(bind2(WorkItemProperties.retrieve))
        find_by_name = staticmethod(bind2(WorkItemProperties.find_by_name))
        find_by_display_name = staticmethod(bind2(WorkItemProperties.find_by_display_name))
        create = staticmethod(bind2(WorkItemProperties.create))
        update = staticmethod(bind2(WorkItemProperties.update))
        delete = staticmethod(bind2(WorkItemProperties.delete))

    class _OwnedWorkflows(Owned["Workflows"]):
        list = staticmethod(bind2(Workflows.list))
        iterate = staticmethod(bind2(Workflows.iterate))
        retrieve = staticmethod(bind2(Workflows.retrieve))
        find_by_name = staticmethod(bind2(Workflows.find_by_name))
        create = staticmethod(bind2(Workflows.create))
        update = staticmethod(bind2(Workflows.update))
        delete = staticmethod(bind2(Workflows.delete))


class LoadedProject(Loaded, Project):
    """A project row that is also the place its children live.

    Every one of the nineteen resources `Projects.__init__` attaches is reachable
    here, so `project.cycles.list()` works exactly the way `project.states.list()`
    does. `tests/v2/test_loaded_navigation.py` compares the two sets and fails if a
    later plan attaches a child without giving its rows a way to reach it."""

    model_config = {**Project.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Declared for the type checker only: a runtime annotation here would make
        # pydantic treat it as a private attribute. `Projects._load` sets it with
        # `object.__setattr__`.
        _resources: Projects

    @property
    def states(self) -> _OwnedStates:
        return cast("_OwnedStates", Owned(self._resources.states, self._ids, self._id_names))

    @property
    def labels(self) -> _OwnedLabels:
        return cast("_OwnedLabels", Owned(self._resources.labels, self._ids, self._id_names))

    @property
    def work_items(self) -> _OwnedWorkItems:
        return cast("_OwnedWorkItems", Owned(self._resources.work_items, self._ids, self._id_names))

    @property
    def cycles(self) -> _OwnedCycles:
        return cast("_OwnedCycles", Owned(self._resources.cycles, self._ids, self._id_names))

    @property
    def milestones(self) -> _OwnedMilestones:
        return cast(
            "_OwnedMilestones", Owned(self._resources.milestones, self._ids, self._id_names)
        )

    @property
    def modules(self) -> _OwnedModules:
        return cast("_OwnedModules", Owned(self._resources.modules, self._ids, self._id_names))

    @property
    def estimates(self) -> _OwnedEstimates:
        return cast("_OwnedEstimates", Owned(self._resources.estimates, self._ids, self._id_names))

    @property
    def intakes(self) -> _OwnedIntakes:
        return cast("_OwnedIntakes", Owned(self._resources.intakes, self._ids, self._id_names))

    @property
    def members(self) -> _OwnedProjectMembers:
        return cast(
            "_OwnedProjectMembers", Owned(self._resources.members, self._ids, self._id_names)
        )

    @property
    def views(self) -> _OwnedProjectViews:
        return cast("_OwnedProjectViews", Owned(self._resources.views, self._ids, self._id_names))

    @property
    def features(self) -> _OwnedProjectFeatures:
        return cast(
            "_OwnedProjectFeatures", Owned(self._resources.features, self._ids, self._id_names)
        )

    @property
    def permissions(self) -> _OwnedProjectPermissions:
        return cast(
            "_OwnedProjectPermissions",
            Owned(self._resources.permissions, self._ids, self._id_names),
        )

    @property
    def work_item_templates(self) -> _OwnedProjectWorkItemTemplates:
        return cast(
            "_OwnedProjectWorkItemTemplates",
            Owned(self._resources.work_item_templates, self._ids, self._id_names),
        )

    @property
    def worklogs(self) -> _OwnedProjectWorklogs:
        return cast(
            "_OwnedProjectWorklogs", Owned(self._resources.worklogs, self._ids, self._id_names)
        )

    @property
    def pages(self) -> _OwnedProjectPages:
        return cast("_OwnedProjectPages", Owned(self._resources.pages, self._ids, self._id_names))

    @property
    def automations(self) -> _OwnedProjectAutomations:
        return cast(
            "_OwnedProjectAutomations",
            Owned(self._resources.automations, self._ids, self._id_names),
        )

    @property
    def work_item_types(self) -> _OwnedWorkItemTypes:
        return cast(
            "_OwnedWorkItemTypes",
            Owned(self._resources.work_item_types, self._ids, self._id_names),
        )

    @property
    def work_item_properties(self) -> _OwnedWorkItemProperties:
        return cast(
            "_OwnedWorkItemProperties",
            Owned(self._resources.work_item_properties, self._ids, self._id_names),
        )

    @property
    def workflows(self) -> _OwnedWorkflows:
        return cast("_OwnedWorkflows", Owned(self._resources.workflows, self._ids, self._id_names))
