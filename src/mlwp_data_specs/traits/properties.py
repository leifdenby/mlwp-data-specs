"""Trait definitions adapted from mxalign properties."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Space(str, Enum):
    GRID = "grid"
    POINT = "point"


class Time(str, Enum):
    FORECAST = "forecast"
    OBSERVATION = "observation"


class Uncertainty(str, Enum):
    DETERMINISTIC = "deterministic"
    ENSEMBLE = "ensemble"
    QUANTILE = "quantile"


@dataclass(frozen=True)
class TraitSelection:
    space: Space | None = None
    time: Time | None = None
    uncertainty: Uncertainty | None = None
