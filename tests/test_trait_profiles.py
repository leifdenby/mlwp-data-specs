"""Tests for the string-valued trait profile classes."""

from __future__ import annotations

from pathlib import Path

import xarray as xr

from mlwp_data_specs import validate_dataset
from mlwp_data_specs.api import SPACE_TRAIT_ATTR
from mlwp_data_specs.trait_profiles import Space, StrEnumLike, Time, Uncertainty


def test_profiles_iterate_in_definition_order() -> None:
    """Iterating a profiles class yields its member values in definition order."""
    assert list(Space) == [Space.GRID, Space.POINT]
    assert list(Time) == [Time.FORECAST, Time.OBSERVATION]
    assert list(Uncertainty) == [
        Uncertainty.DETERMINISTIC,
        Uncertainty.ENSEMBLE,
        Uncertainty.QUANTILE,
    ]


def test_profiles_membership() -> None:
    """`in` checks a value against the member values."""
    assert Space.GRID in Space
    assert Time.FORECAST not in Space
    assert "not_a_profile" not in Space


def test_profile_members_are_plain_str() -> None:
    """Members are plain `str` objects, not enum members."""
    for profiles_cls in (Space, Time, Uncertainty):
        for value in profiles_cls:
            assert type(value) is str


def test_profiles_inherit_members() -> None:
    """Members defined on a parent class are included when iterating."""

    class ParentProfiles(StrEnumLike):
        A = "a"

    class ChildProfiles(ParentProfiles):
        B = "b"

    assert list(ChildProfiles) == ["a", "b"]


def test_profile_attribute_round_trips_through_zarr(tmp_path: Path) -> None:
    """A profile set as a dataset attribute is saved and read back without casting.

    Parameters
    ----------
    tmp_path : Path
        Temporary directory provided by pytest.
    """
    ds_grid = xr.Dataset(
        coords={
            "longitude": ("longitude", [10.0, 11.0]),
            "latitude": ("latitude", [60.0, 61.0]),
        }
    )
    ds_grid.coords["longitude"].attrs.update(
        {"standard_name": "longitude", "units": "degrees_east"}
    )
    ds_grid.coords["latitude"].attrs.update(
        {"standard_name": "latitude", "units": "degrees_north"}
    )
    ds_grid.attrs[SPACE_TRAIT_ATTR] = Space.GRID

    path = tmp_path / "grid.zarr"
    ds_grid.to_zarr(path)
    ds_reopened = xr.open_zarr(path)

    assert ds_reopened.attrs[SPACE_TRAIT_ATTR] == Space.GRID
    assert not validate_dataset(ds_reopened).has_fails()
