"""Supported trait profiles for each trait axis.

This module has no internal imports so that both the trait specifications and
the checks can use the profile names without import cycles.
"""

from __future__ import annotations

from collections.abc import Iterator


class _StrEnumLikeMeta(type):
    """Metaclass making `StrEnumLike` classes iterable and support ``in``.

    This has to be a metaclass because ``for value in Space`` and
    ``value in Space`` look up ``__iter__``/``__contains__`` on the type of the
    class (its metaclass), not on the class itself.
    """

    def __iter__(cls) -> Iterator[str]:
        """Iterate over the member values, in definition order.

        Members are the upper-case class attributes with ``str`` values,
        including those inherited from parent classes.

        Yields
        ------
        str
            Member values.
        """
        seen: set[str] = set()
        for klass in reversed(cls.__mro__):
            for name, value in vars(klass).items():
                if name.isupper() and isinstance(value, str) and value not in seen:
                    seen.add(value)
                    yield value

    def __contains__(cls, value: object) -> bool:
        """Check whether a value is one of the member values.

        Parameters
        ----------
        value : object
            Value to look up.

        Returns
        -------
        bool
            ``True`` if ``value`` equals one of the member values.
        """
        return value in list(cls)


class StrEnumLike(metaclass=_StrEnumLikeMeta):
    """Enum-like namespace whose members are plain ``str`` values.

    Trait profiles are stored as global attributes on datasets (e.g.
    ``ds.attrs["mlwp_space_trait"] = Space.GRID``). Members of an ``enum.Enum``
    (including ``str``-mixin enums and ``enum.StrEnum``) are not plain ``str``
    objects, so they have to be cast (``.value``) before a dataset can be
    written to netCDF/zarr, and they format differently across Python versions.
    Members of a `StrEnumLike` subclass *are* plain strings, so they can be set
    as attributes and serialised directly, while the class still behaves like an
    enum for iteration (``list(Space)``) and membership (``"grid" in Space``).

    Subclasses define their members as upper-case class attributes::

        class Space(StrEnumLike):
            GRID = "grid"
            POINT = "point"
    """


class Space(StrEnumLike):
    """Supported spatial trait profiles."""

    GRID = "grid"
    POINT = "point"


class Time(StrEnumLike):
    """Supported temporal trait profiles."""

    FORECAST = "forecast"
    OBSERVATION = "observation"


class Uncertainty(StrEnumLike):
    """Supported uncertainty trait profiles."""

    DETERMINISTIC = "deterministic"
    ENSEMBLE = "ensemble"
    QUANTILE = "quantile"
