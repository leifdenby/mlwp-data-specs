"""Loader hooks for ``anemoi-datasets`` stores."""

from __future__ import annotations

import numpy as np
import xarray as xr

DROP_VARS = [
    "latitude",
    "longitude",
    "time",
    "cos_julian_day",
    "cos_latitude",
    "cos_local_time",
    "cos_longitude",
    "insolation",
    "sin_julian_day",
    "sin_latitude",
    "sin_local_time",
    "sin_longitude",
]

COORDS = {
    "longitude": "longitudes",
    "latitude": "latitudes",
    "valid_time": "dates",
}

OPEN_KWARGS = {"engine": "zarr", "consolidated": False}
CONCAT_DIM = "valid_time"


def preprocess(dataset: xr.Dataset) -> xr.DataArray:
    """Normalize one ``anemoi-datasets`` input before concatenation.

    Parameters
    ----------
    dataset : xr.Dataset
        Raw dataset opened from one Zarr input.

    Returns
    -------
    xr.DataArray
        Normalized array with harmonized coordinates and dimensions.
    """
    coords = {
        key: dataset[value].astype("datetime64[ns]").load()
        if key == "valid_time"
        else dataset[value].load()
        for key, value in COORDS.items()
    }
    coords["latitude"] = coords["latitude"].astype(np.float32)
    coords["longitude"] = coords["longitude"].astype(np.float32)
    coords["variable"] = dataset.attrs["variables"]
    coords["valid_time"] = coords["valid_time"].astype("datetime64[ns]")

    drop_vars = [var for var in DROP_VARS if var in coords["variable"]]

    return (
        dataset.assign_coords(coords)["data"]
        .isel(ensemble=0)
        .drop_sel(variable=drop_vars)
        .swap_dims({"time": "valid_time"})
        .rename({"cell": "grid_index"})
    )


def postprocess(ds: xr.DataArray) -> xr.Dataset:
    """Convert the concatenated data array into a validation dataset.

    Parameters
    ----------
    ds : xr.DataArray
        Concatenated array across ``valid_time``.

    Returns
    -------
    xr.Dataset
        Dataset keyed by variable name.
    """
    return ds.to_dataset(dim="variable")
