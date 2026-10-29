"""Uncertainty coordinate metadata checks."""

from __future__ import annotations

import xarray as xr

from mlwp_data_specs.checks.coords.names import check_coordinate_attrs
from mlwp_data_specs.specs.reporting import ValidationReport, log_function_call
from mlwp_data_specs.trait_profiles import Uncertainty


@log_function_call
def check_uncertainty_coordinate_metadata(
    ds: xr.Dataset,
    *,
    trait: str,
) -> ValidationReport:
    """Validate coordinate metadata for the selected uncertainty trait.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset being validated.
    trait : str
        Selected uncertainty profile, one of the `Uncertainty` members.

    Returns
    -------
    ValidationReport
        Report for uncertainty coordinate metadata and bounds checks.
    """
    report = ValidationReport()
    section = "Uncertainty"

    if trait == Uncertainty.DETERMINISTIC:
        report.add(
            section,
            "Deterministic mode metadata",
            "PASS",
            "No uncertainty coordinate required",
        )
        return report

    if trait == Uncertainty.ENSEMBLE:
        report += check_coordinate_attrs(
            ds,
            section=section,
            requirement="Metadata for coordinate 'member'",
            coord="member",
            required_attrs={"standard_name": {"realization"}},
        )
        return report

    report += check_coordinate_attrs(
        ds,
        section=section,
        requirement="Metadata for coordinate 'quantile'",
        coord="quantile",
        required_attrs={"standard_name": {"quantile"}, "units": {"1"}},
    )

    if "quantile" not in ds.coords:
        return report

    quantile_values = ds.coords["quantile"].values
    invalid = [float(v) for v in quantile_values if float(v) < 0.0 or float(v) > 1.0]
    if invalid:
        report.add(
            section,
            "Quantile bounds",
            "FAIL",
            f"Quantile values must be in [0, 1], found {invalid}",
        )
    else:
        report.add(section, "Quantile bounds", "PASS", "All quantiles are in [0, 1]")

    return report
