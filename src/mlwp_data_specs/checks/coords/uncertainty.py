"""Uncertainty coordinate metadata checks."""

from __future__ import annotations

import xarray as xr

from mlwp_data_specs.checks.coords.names import check_coordinate_attrs
from mlwp_data_specs.specs.reporting import ValidationReport, log_function_call


@log_function_call
def check_uncertainty_coordinate_metadata(
    ds: xr.Dataset,
    *,
    trait: object,
) -> ValidationReport:
    """Validate coordinate metadata for the selected uncertainty trait.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset being validated.
    trait : object
        Selected uncertainty profile enum instance (or enum-like object with a
        ``value`` attribute).

    Returns
    -------
    ValidationReport
        Report for uncertainty coordinate metadata and bounds checks.
    """
    report = ValidationReport()
    section = "Uncertainty"

    trait_value = str(getattr(trait, "value", trait))
    if trait_value == "deterministic":
        report.add(
            section,
            "Deterministic mode metadata",
            "PASS",
            "No uncertainty coordinate required",
        )
        return report

    if trait_value == "ensemble":
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
