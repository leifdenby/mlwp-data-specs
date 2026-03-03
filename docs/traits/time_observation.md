---
trait: time_coordinate
profile: observation
version: 0.1.0
---

## 1. Scope

This specification enforces time-coordinate trait conformance for machine-learning weather datasets.

## 2. Structural Requirements

- The dataset MUST provide required time dimensions and coordinate names for the selected time trait profile.

## 3. Coordinate Metadata Requirements

- Time coordinates MUST expose CF-compatible metadata.
- `standard_name` MUST be set for required time coordinates.
- For forecast lead times, units MUST indicate elapsed time.
