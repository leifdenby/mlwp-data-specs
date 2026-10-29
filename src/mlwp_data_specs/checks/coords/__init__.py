"""Checks on dataset coordinates and dimensions."""

from __future__ import annotations

from typing import Literal

TraitAxis = Literal["space", "time", "uncertainty"]

SECTION_MAP: dict[TraitAxis, str] = {
    "space": "Spatial Coordinate",
    "time": "Time Coordinate",
    "uncertainty": "Uncertainty",
}
