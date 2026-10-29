"""Tests for global attribute checks."""

from __future__ import annotations

import pytest
import xarray as xr

from mlwp_data_specs.checks.global_attributes.traits import check_trait_attribute
from mlwp_data_specs.specs.traits.time_coordinate import Time


@pytest.mark.parametrize(
    ("attrs", "expected_status"),
    [
        ({}, "PASS"),
        ({"mlwp_time_trait": "forecast"}, "PASS"),
        ({"mlwp_time_trait": "observation"}, "WARNING"),
        ({"mlwp_time_trait": "nowcast"}, "FAIL"),
        ({"mlwp_time_trait": Time.FORECAST}, "PASS"),
        ({"mlwp_time_trait": Time.OBSERVATION}, "WARNING"),
    ],
)
def test_check_trait_attribute(attrs: dict[str, str], expected_status: str) -> None:
    """Absent or matching attributes pass, mismatches warn, invalid values fail."""
    ds = xr.Dataset(attrs=attrs)
    report = check_trait_attribute(ds, trait_axis="time", trait=Time.FORECAST)

    assert [r.status for r in report.results] == [expected_status]
    assert report.results[0].section == "Time Coordinate"
