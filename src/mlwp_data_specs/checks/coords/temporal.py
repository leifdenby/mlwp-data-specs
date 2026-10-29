"""Time coordinate metadata checks."""

from __future__ import annotations

import xarray as xr

from mlwp_data_specs.checks.coords.names import check_coordinate_attrs
from mlwp_data_specs.specs.reporting import ValidationReport, log_function_call
from mlwp_data_specs.trait_profiles import Time


@log_function_call
def check_time_coordinate_metadata(ds: xr.Dataset, *, trait: str) -> ValidationReport:
    """Validate coordinate metadata for the selected time trait.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset being validated.
    trait : str
        Selected time profile, one of the `Time` members.

    Returns
    -------
    ValidationReport
        Combined report for all required time coordinates.
    """
    report = ValidationReport()
    section = "Time Coordinate"

    expectations: dict[str, dict[str, set[str]]] = {}
    if trait == Time.OBSERVATION:
        expectations["valid_time"] = {
            "standard_name": {"time"},
        }
    elif trait == Time.FORECAST:
        expectations.update(
            {
                "reference_time": {
                    "standard_name": {"forecast_reference_time", "time"},
                },
                "lead_time": {
                    "standard_name": {"forecast_period"},
                    "units": {"s", "seconds", "h", "hours"},
                },
            }
        )

    for coord, required_attrs in expectations.items():
        report += check_coordinate_attrs(
            ds,
            section=section,
            requirement=f"Metadata for coordinate '{coord}'",
            coord=coord,
            required_attrs=required_attrs,
        )

    if "valid_time" in ds.coords and trait == Time.FORECAST:
        report += check_coordinate_attrs(
            ds,
            section=section,
            requirement="Metadata for coordinate 'valid_time'",
            coord="valid_time",
            required_attrs={"standard_name": {"time"}},
        )

    return report
