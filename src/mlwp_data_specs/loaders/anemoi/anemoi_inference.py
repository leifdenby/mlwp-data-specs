"""Loader for reading multiple NetCDF files produced by ``anemoi-inference``.

The hooks in this module combine per-run inference outputs into an
``xarray.Dataset`` that conforms to the structural expectations of
``mlwp-data-specs``.
"""

from __future__ import annotations

import xarray as xr

OPEN_KWARGS = {"engine": "h5netcdf", "chunks": "auto"}
CONCAT_DIM = "reference_time"
valid_time_profiles = ("forecast",)
valid_space_profiles = ("grid",)
valid_uncertainty_profiles = ("deterministic",)


def preprocess(ds: xr.Dataset) -> xr.Dataset:
    """Normalize one inference output before concatenation.

    Parameters
    ----------
    ds : xr.Dataset
        Raw dataset opened from one source file/store.

    Returns
    -------
    xr.Dataset
        Dataset with explicit ``reference_time`` and spatial coordinates.
    """
    return (
        ds.set_coords(["longitude", "latitude"])
        .expand_dims("reference_time")
        .assign_coords({"reference_time": ("reference_time", [ds["time"].values[0]])})
    )


def postprocess(ds: xr.Dataset) -> xr.Dataset:
    """Add ``lead_time`` and grid dimension metadata after concatenation.

    Parameters
    ----------
    ds : xr.Dataset
        Concatenated inference dataset.

    Returns
    -------
    xr.Dataset
        Dataset with ``lead_time`` and ``grid_index`` dimensions.
    """
    lead_times = ds["time"].values - ds["time"].values[0]
    return (
        ds.assign_coords({"lead_time": ("time", lead_times)})
        .rename_dims({"values": "grid_index"})
        .swap_dims({"time": "lead_time"})
    )
