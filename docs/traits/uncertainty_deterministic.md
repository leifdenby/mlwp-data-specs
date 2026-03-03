---
trait: uncertainty
profile: deterministic
version: 0.1.0
---

## 1. Scope

This specification enforces uncertainty representation requirements.

## 2. Structural Requirements

- Deterministic datasets MAY omit uncertainty coordinates.
- Ensemble datasets MUST provide `member` coordinate support.
- Quantile datasets MUST provide `quantile` coordinate support.

## 3. Coordinate Metadata Requirements

- Ensemble mode SHOULD represent realization members with CF-compliant metadata.
- Quantile mode MUST provide `quantile` metadata and quantile values in [0, 1].
