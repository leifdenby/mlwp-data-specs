# AGENTS

Guidance for agents and contributors working in this repository.

## Project intent

- `mlwp-data-specs` defines and validates trait-based dataset specifications.
- Validation is split from alignment:
  - this repo validates structure/metadata contracts
  - `mxalign` performs alignment operations

## Interfaces

- Python API: `validate_dataset(...)`
- CLI: `mlwp.validate_dataset_traits`

## Common commands

- Install/sync env: `uv sync`
- Run tests: `uv run python -m pytest`
- Regenerate trait docs: `uv run python docs/scripts/generate_trait_docs.py`
- Build docs: `uv run mkdocs build -f docs/mkdocs.yml --strict`

## Structure

- Trait specs: `src/mlwp_data_specs/specs/traits/`
- Shared checks: `src/mlwp_data_specs/checks/`
- CLI/reporting: `src/mlwp_data_specs/specs/`
- Docs generator: `docs/scripts/generate_trait_docs.py`

## Development expectations

- Keep inline spec text and executable checks synchronized.
- Add/update tests when changing behavior.
- Keep docstrings and type annotations on new code.
