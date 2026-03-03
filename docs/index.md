# MLWP Trait Specifications

Generated from inline executable specs in `mlwp-data-specs` 0.1.0.

## Requirements

- The validator checks selected dataset traits: `time`, `space`, `uncertainty`.
- Checks include structural constraints and metadata constraints.
- Trait specs remain executable and are rendered as documentation.

## Interfaces

Both interfaces are expected:

1. Python API via `check_dataset(ds, time=..., space=..., uncertainty=...)`.
2. CLI via `mlwp.validate_trait` for local/remote validation and CI usage.

## Available Spec Pages

- space
  - [grid](traits/space_grid.md)
  - [point](traits/space_point.md)
- time
  - [forecast](traits/time_forecast.md)
  - [observation](traits/time_observation.md)
- uncertainty
  - [deterministic](traits/uncertainty_deterministic.md)
  - [ensemble](traits/uncertainty_ensemble.md)
  - [quantile](traits/uncertainty_quantile.md)
