"""Structural trait checks based on allowed dims and required coordinates."""

from __future__ import annotations

from mlwp_data_specs.traits.properties import Space, Time, Uncertainty
from mlwp_data_specs.traits.reporting import ValidationReport, log_function_call
from mlwp_data_specs.traits.specs import SPACE_SPECS, TIME_SPECS, UNCERTAINTY_SPECS


SECTION_MAP = {
    "space": "Spatial Coordinate",
    "time": "Time Coordinate",
    "uncertainty": "Uncertainty",
}


@log_function_call
def check_dim_variants(ds, *, axis: str, variants: list[set[str]]) -> ValidationReport:
    report = ValidationReport()
    requirement = "Allowed dimension variants"

    if not variants:
        report.add(SECTION_MAP[axis], requirement, "PASS", "No dimension restrictions")
        return report

    ds_dims = set(ds.dims)
    for variant in variants:
        if variant.issubset(ds_dims):
            report.add(
                SECTION_MAP[axis],
                requirement,
                "PASS",
                f"Dataset dims satisfy variant {sorted(variant)}",
            )
            return report

    report.add(
        SECTION_MAP[axis],
        requirement,
        "FAIL",
        f"Dataset dims {sorted(ds_dims)} do not match any allowed variants",
    )
    return report


@log_function_call
def check_required_coords(ds, *, axis: str, required_coords: set[str]) -> ValidationReport:
    report = ValidationReport()
    requirement = "Required coordinates are present"

    if not required_coords:
        report.add(SECTION_MAP[axis], requirement, "PASS", "No required coordinates")
        return report

    missing = required_coords - set(ds.coords)
    if missing:
        report.add(
            SECTION_MAP[axis],
            requirement,
            "FAIL",
            f"Missing required coordinates: {sorted(missing)}",
        )
    else:
        report.add(
            SECTION_MAP[axis],
            requirement,
            "PASS",
            f"All required coordinates present: {sorted(required_coords)}",
        )
    return report


@log_function_call
def check_space_trait_structure(ds, *, trait: Space) -> ValidationReport:
    spec = SPACE_SPECS[trait]
    report = ValidationReport()
    report += check_dim_variants(ds, axis="space", variants=spec.dim_variants)
    report += check_required_coords(ds, axis="space", required_coords=spec.required_coords)
    return report


@log_function_call
def check_time_trait_structure(ds, *, trait: Time) -> ValidationReport:
    spec = TIME_SPECS[trait]
    report = ValidationReport()
    report += check_dim_variants(ds, axis="time", variants=spec.dim_variants)
    report += check_required_coords(ds, axis="time", required_coords=spec.required_coords)
    return report


@log_function_call
def check_uncertainty_trait_structure(ds, *, trait: Uncertainty) -> ValidationReport:
    spec = UNCERTAINTY_SPECS[trait]
    report = ValidationReport()
    report += check_dim_variants(ds, axis="uncertainty", variants=spec.dim_variants)
    report += check_required_coords(
        ds,
        axis="uncertainty",
        required_coords=spec.required_coords,
    )
    return report
