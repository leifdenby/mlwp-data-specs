"""Spatial coordinate metadata checks."""

from __future__ import annotations

import xarray as xr

from mlwp_data_specs.checks.coords.names import check_coordinate_attrs
from mlwp_data_specs.specs.reporting import ValidationReport, log_function_call


@log_function_call
def check_space_coordinate_metadata(
    ds: xr.Dataset, *, trait: object
) -> ValidationReport:
    """Validate coordinate metadata for the selected space trait.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset being validated.
    trait : object
        Selected space profile enum instance (or enum-like object with a
        ``value`` attribute).

    Returns
    -------
    ValidationReport
        Combined report for all relevant spatial coordinates.
    """
    report = ValidationReport()
    section = "Spatial Coordinate"

    expectations = {
        "longitude": {
            "standard_name": {"longitude"},
            "units": {"degrees_east"},
        },
        "latitude": {
            "standard_name": {"latitude"},
            "units": {"degrees_north"},
        },
    }
    trait_value = str(getattr(trait, "value", trait))
    if trait_value == "grid":
        expectations.update(
            {
                "xc": {
                    "standard_name": {"projection_x_coordinate"},
                    "units": {"m", "meter", "metre"},
                },
                "yc": {
                    "standard_name": {"projection_y_coordinate"},
                    "units": {"m", "meter", "metre"},
                },
            }
        )

    for coord, required_attrs in expectations.items():
        if coord not in ds.coords and coord in {"xc", "yc"}:
            continue
        report += check_coordinate_attrs(
            ds,
            section=section,
            requirement=f"Metadata for coordinate '{coord}'",
            coord=coord,
            required_attrs=required_attrs,
        )

    return report
