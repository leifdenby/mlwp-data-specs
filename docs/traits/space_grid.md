---
trait: spatial_coordinate
profile: grid
version: 0.1.0
---

## 1. Scope

This specification enforces spatial-coordinate trait conformance for gridded and point datasets.

## 2. Structural Requirements

- The dataset MUST provide dimensions and coordinates accepted by the selected spatial trait profile.
- Required spatial coordinates MUST be present.

## 3. Coordinate Metadata Requirements

- Longitude/latitude coordinates MUST carry CF-compatible `standard_name` and angular units.
- If projected coordinates are present (`xc`, `yc`), they MUST expose projection coordinate metadata.
