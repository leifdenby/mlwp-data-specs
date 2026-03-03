"""CLI entry point for MLWP trait validation."""

from __future__ import annotations

import argparse
from collections.abc import Sequence

import xarray as xr
from loguru import logger

from mlwp_data_specs import __version__
from mlwp_data_specs.traits.properties import Space, Time, Uncertainty
from mlwp_data_specs.traits.reporting import ValidationReport, skip_all_checks
from mlwp_data_specs.traits.spatial_coordinate import validate_dataset as validate_space
from mlwp_data_specs.traits.time_coordinate import validate_dataset as validate_time
from mlwp_data_specs.traits.uncertainty import validate_dataset as validate_uncertainty


def _choice_values(enum_cls) -> list[str]:
    return sorted(item.value for item in enum_cls)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a dataset against selected trait specs. "
            "At least one of --space/--time/--uncertainty must be provided."
        )
    )
    parser.add_argument("dataset_path", nargs="?", help="Path/URL to dataset (zarr)")
    parser.add_argument("--space", choices=_choice_values(Space), help="Space trait name")
    parser.add_argument("--time", choices=_choice_values(Time), help="Time trait name")
    parser.add_argument(
        "--uncertainty",
        choices=_choice_values(Uncertainty),
        help="Uncertainty trait name",
    )
    parser.add_argument(
        "--s3-endpoint-url",
        default=None,
        help="Optional S3 endpoint URL for opening the dataset",
    )
    parser.add_argument("--s3-anon", action="store_true", help="Use anonymous S3 access")
    parser.add_argument(
        "--print-spec-markdown",
        action="store_true",
        help="Print selected trait specs without running checks",
    )
    parser.add_argument("--list-space", action="store_true", help="List supported space trait values")
    parser.add_argument("--list-time", action="store_true", help="List supported time trait values")
    parser.add_argument(
        "--list-uncertainty",
        action="store_true",
        help="List supported uncertainty trait values",
    )
    return parser


def _print_list(title: str, values: list[str]) -> None:
    print(title)
    for value in values:
        print(f"  - {value}")


def _run_selected_validations(ds, *, space: Space | None, time: Time | None, uncertainty: Uncertainty | None):
    report = ValidationReport()
    spec_texts: list[str] = []

    if space is not None:
        trait_report, spec = validate_space(ds, trait=space)
        report += trait_report
        spec_texts.append(spec)

    if time is not None:
        trait_report, spec = validate_time(ds, trait=time)
        report += trait_report
        spec_texts.append(spec)

    if uncertainty is not None:
        trait_report, spec = validate_uncertainty(ds, trait=uncertainty)
        report += trait_report
        spec_texts.append(spec)

    return report, spec_texts


@logger.catch
def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.list_space:
        _print_list("Supported space traits:", _choice_values(Space))
        return 0
    if args.list_time:
        _print_list("Supported time traits:", _choice_values(Time))
        return 0
    if args.list_uncertainty:
        _print_list("Supported uncertainty traits:", _choice_values(Uncertainty))
        return 0

    space = Space(args.space) if args.space else None
    time = Time(args.time) if args.time else None
    uncertainty = Uncertainty(args.uncertainty) if args.uncertainty else None

    if not any([space, time, uncertainty]):
        parser.error("At least one trait must be selected with --space/--time/--uncertainty")

    if not args.print_spec_markdown and not args.dataset_path:
        parser.error("dataset_path is required unless --print-spec-markdown is used")

    logger.info(f"Running mlwp-data-specs {__version__}")

    if args.print_spec_markdown:
        with skip_all_checks():
            _, specs = _run_selected_validations(
                ds=None,
                space=space,
                time=time,
                uncertainty=uncertainty,
            )
        print("\n\n".join(text.strip() for text in specs if text.strip()))
        return 0

    storage_options = {}
    if args.s3_endpoint_url:
        storage_options["endpoint_url"] = args.s3_endpoint_url
    if args.s3_anon:
        storage_options["anon"] = True

    ds = xr.open_zarr(args.dataset_path, storage_options=storage_options or None)
    if storage_options:
        ds.encoding.setdefault("storage_options", storage_options)

    report, _ = _run_selected_validations(
        ds=ds,
        space=space,
        time=time,
        uncertainty=uncertainty,
    )
    report.console_print()

    return 1 if report.has_fails() else 0


if __name__ == "__main__":
    raise SystemExit(main())
