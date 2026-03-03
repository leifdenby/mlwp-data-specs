"""Executable specification for uncertainty traits."""

from __future__ import annotations

import textwrap

from mlwp_data_specs.checks.metadata.coords import check_uncertainty_coordinate_metadata
from mlwp_data_specs.checks.traits.structure import check_uncertainty_trait_structure
from mlwp_data_specs.traits.properties import Uncertainty
from mlwp_data_specs.traits.reporting import ValidationReport

VERSION = "0.1.0"
IDENTIFIER = "uncertainty"


def validate_dataset(ds, *, trait: Uncertainty) -> tuple[ValidationReport, str]:
    """Validate dataset against uncertainty trait requirements."""
    report = ValidationReport()
    spec_text = f"""
    ---
    trait: {IDENTIFIER}
    profile: {trait.value}
    version: {VERSION}
    ---

    ## 1. Scope

    This specification enforces uncertainty representation requirements.

    ## 2. Structural Requirements

    - Deterministic datasets MAY omit uncertainty coordinates.
    - Ensemble datasets MUST provide `member` coordinate support.
    - Quantile datasets MUST provide `quantile` coordinate support.
    """

    report += check_uncertainty_trait_structure(ds, trait=trait)

    spec_text += """
    ## 3. Coordinate Metadata Requirements

    - Ensemble mode SHOULD represent realization members with CF-compliant metadata.
    - Quantile mode MUST provide `quantile` metadata and quantile values in [0, 1].
    """

    report += check_uncertainty_coordinate_metadata(ds, trait=trait)

    return report, textwrap.dedent(spec_text)
