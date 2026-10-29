"""Tests for public Python API entry points."""

from __future__ import annotations

from importlib.metadata import version
from unittest.mock import patch

import pytest
import xarray as xr

from mlwp_data_specs import __version__, validate_dataset
from mlwp_data_specs.api import SPACE_TRAIT_ATTR, TIME_TRAIT_ATTR
from mlwp_data_specs.specs.traits.spatial_coordinate import Space
from mlwp_data_specs.specs.traits.time_coordinate import Time


def _forecast_grid_ds() -> xr.Dataset:
    """Create a forecast + grid dataset that satisfies selected checks.

    Returns
    -------
    xr.Dataset
        Test dataset instance.
    """
    ds = xr.Dataset(
        coords={
            "reference_time": ("reference_time", [0]),
            "lead_time": ("lead_time", [1]),
            "longitude": ("longitude", [10.0, 11.0]),
            "latitude": ("latitude", [60.0, 61.0]),
        }
    )
    ds.coords["reference_time"].attrs["standard_name"] = "forecast_reference_time"
    ds.coords["lead_time"].attrs.update(
        {"standard_name": "forecast_period", "units": "hours"}
    )
    ds.coords["longitude"].attrs.update(
        {"standard_name": "longitude", "units": "degrees_east"}
    )
    ds.coords["latitude"].attrs.update(
        {"standard_name": "latitude", "units": "degrees_north"}
    )
    return ds


def test_validate_dataset_accepts_string_traits() -> None:
    """API accepts string trait selectors and returns a passing report."""
    report = validate_dataset(_forecast_grid_ds(), time="forecast", space="grid")
    assert not report.has_fails()


def test_package_version_matches_metadata() -> None:
    """Package exposes the installed distribution version."""
    assert __version__ == version("mlwp-data-specs")


def test_validate_dataset_requires_trait() -> None:
    """API raises when no traits are selected."""
    with pytest.raises(ValueError, match="At least one trait"):
        validate_dataset(_forecast_grid_ds())


def test_validate_dataset_from_attributes() -> None:
    """Traits can be loaded from global dataset attributes."""
    ds = _forecast_grid_ds()
    ds.attrs[TIME_TRAIT_ATTR] = "forecast"
    ds.attrs[SPACE_TRAIT_ATTR] = "grid"

    report = validate_dataset(ds)
    assert not report.has_fails()


@patch("mlwp_data_specs.api.logger")
def test_validate_dataset_attribute_mismatch_warning(mock_logger) -> None:
    """Mismatch between provided argument and attribute logs a warning."""
    ds = _forecast_grid_ds()
    # The dataset has forecast coords, but we put "observation" in the attribute
    ds.attrs[TIME_TRAIT_ATTR] = "observation"

    # We pass time="forecast" to override the attribute
    report = validate_dataset(ds, time="forecast", space="grid")

    # Should not fail because "forecast" is used for validation, but the
    # mismatching attribute is reported as a warning
    assert not report.has_fails()
    assert report.has_warnings()

    # Check that a warning was emitted
    mock_logger.warning.assert_called()
    warning_msg = mock_logger.warning.call_args[0][0]
    assert "Provided time trait 'forecast' differs" in warning_msg
    assert "attribute 'mlwp_time_trait' ('observation')" in warning_msg


@patch("mlwp_data_specs.api.logger")
def test_validate_dataset_invalid_attribute_warning(mock_logger) -> None:
    """Invalid attribute value logs a warning, falls back to the provided arg and
    is reported as a failure."""
    ds = _forecast_grid_ds()
    ds.attrs[TIME_TRAIT_ATTR] = "invalid_time_trait"

    report = validate_dataset(ds, time="forecast", space="grid")
    failed = [r for r in report.results if r.status == "FAIL"]
    assert [r.requirement for r in failed] == ["Global attribute 'mlwp_time_trait'"]

    mock_logger.warning.assert_called()
    warning_msg = mock_logger.warning.call_args[0][0]
    assert "Invalid trait value in attribute 'mlwp_time_trait'" in warning_msg


def test_validate_dataset_invalid_attribute_unvalidated_trait() -> None:
    """Invalid attribute is reported as a failure even when its trait is not
    validated."""
    ds = _forecast_grid_ds()
    ds.attrs[TIME_TRAIT_ATTR] = "invalid_time_trait"

    report = validate_dataset(ds, space="grid")
    failed = [r for r in report.results if r.status == "FAIL"]
    assert [r.requirement for r in failed] == ["Global attribute 'mlwp_time_trait'"]


def test_validate_dataset_enum_member_attributes() -> None:
    """Attributes set to trait enum members, as the loaders do, pass."""
    ds = _forecast_grid_ds()
    ds.attrs[TIME_TRAIT_ATTR] = Time.FORECAST
    ds.attrs[SPACE_TRAIT_ATTR] = Space.GRID

    report = validate_dataset(ds)
    assert not report.has_fails()
    assert not report.has_warnings()
