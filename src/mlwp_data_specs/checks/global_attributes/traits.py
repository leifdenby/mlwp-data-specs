"""Checks on global attributes declaring dataset trait profiles."""

from __future__ import annotations

from enum import Enum

import xarray as xr

from mlwp_data_specs.checks import SECTION_MAP, TraitAxis
from mlwp_data_specs.specs.reporting import ValidationReport, log_function_call

TRAIT_ATTR_FORMAT = "mlwp_{}_trait"


@log_function_call
def check_trait_attribute(
    ds: xr.Dataset,
    *,
    trait_axis: TraitAxis,
    trait: Enum,
) -> ValidationReport:
    """Validate the optional global attribute declaring a trait profile.

    Parameters
    ----------
    ds : xr.Dataset
        Dataset being validated.
    trait_axis : TraitAxis
        Trait axis key, used to build the attribute name (e.g.
        ``mlwp_time_trait``).
    trait : Enum
        Trait profile the dataset is being validated against.

    Returns
    -------
    ValidationReport
        PASS if the attribute is absent or matches ``trait``, FAIL if it is not
        a valid profile value, WARNING if it names a different valid profile.
    """
    report = ValidationReport()
    section = SECTION_MAP[trait_axis]
    attr_name = TRAIT_ATTR_FORMAT.format(trait_axis)
    requirement = f"Global attribute '{attr_name}'"

    value = ds.attrs.get(attr_name)
    if value is None:
        report.add(section, requirement, "PASS", "Optional attribute not set")
        return report

    allowed = [item.value for item in type(trait)]
    if str(value) not in allowed:
        report.add(
            section,
            requirement,
            "FAIL",
            f"Value '{value}' is not one of {allowed}",
        )
    elif str(value) != trait.value:
        report.add(
            section,
            requirement,
            "WARNING",
            f"Value '{value}' differs from validated profile '{trait.value}'",
        )
    else:
        report.add(section, requirement, "PASS", f"Value '{value}' matches profile")
    return report
