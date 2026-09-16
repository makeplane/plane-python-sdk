"""A row type a caller cannot name is not a public return type.

Every navigable resource's `retrieve`/`list`/`iterate`/`find_by_*`/verb answers a
`Loaded*` row, and those classes lived only in `plane.api.v2._loaded.*` -- a private
package. So the declared return type of a large slice of the public surface could not
be imported without reaching under the underscore: no annotating a variable, a
helper's parameter or a test fixture, and `py.typed` plus the whole typed-navigation
apparatus stopped at the point where a user wanted to *hold* a row.

Found refreshing the live integration suite, where the session-shared project fixture
wants to be annotated `LoadedProject` so its navigation (`project.states.list()`) is
type-checked like everything else.

The sweep is enumerated the same way the other rule sweeps are (see
`tests/v2/tree_walk.py`): over every resource class in the package that declares a
`loaded_model`, so a navigable family added later cannot forget to export its row.
"""

from __future__ import annotations

import plane.api.v2 as v2

from .tree_walk import all_resource_classes


def _declared_loaded_models() -> dict[str, type]:
    """Every `Loaded*` class the package's resources actually answer with."""
    found: dict[str, type] = {}
    for resource_class in all_resource_classes():
        loaded_model = getattr(resource_class, "loaded_model", None)
        if loaded_model is not None:
            found[loaded_model.__name__] = loaded_model
    return found


def test_every_loaded_row_type_is_importable_from_the_public_package() -> None:
    missing = sorted(name for name in _declared_loaded_models() if not hasattr(v2, name))
    assert not missing, (
        f"{len(missing)} row types are returned by public methods but cannot be imported "
        f"from `plane.api.v2`: {missing}. Re-export them there; a caller must not have to "
        "import out of `plane.api.v2._loaded` to name a value the SDK handed them."
    )


def test_every_loaded_row_type_is_named_in_dunder_all() -> None:
    exported = set(v2.__all__)
    missing = sorted(name for name in _declared_loaded_models() if name not in exported)
    assert not missing, (
        f"Row types importable from `plane.api.v2` but absent from its `__all__`: {missing}. "
        "`__all__` is what a star-import and the docs tooling see."
    )


def test_the_export_is_the_same_object_the_resources_return() -> None:
    """Re-exporting a *different* class of the same name would type-check and lie."""
    for name, loaded_model in sorted(_declared_loaded_models().items()):
        assert (
            getattr(v2, name) is loaded_model
        ), f"`plane.api.v2.{name}` is not the class the resources answer with."


def test_there_are_no_stale_loaded_exports() -> None:
    """A `Loaded*` name in `__all__` that no resource returns any more is dead surface."""
    declared = set(_declared_loaded_models())
    exported = {name for name in v2.__all__ if name.startswith("Loaded")}
    assert (
        exported - declared == set()
    ), f"Exported but returned by nothing: {sorted(exported - declared)}."
