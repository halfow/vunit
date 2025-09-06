# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2025, Lars Asplund lars.anders.asplund@gmail.com

"""
Contains type defining VHDL standards and operations on them
"""

from __future__ import annotations

from enum import IntEnum


class VHDLStandard(IntEnum):
    """VHDL Standards."""
    STD_1993 = 1993
    STD_2002 = 2002
    STD_2008 = 2008
    STD_2019 = 2019

    def __str__(self) -> str:
        # For backwards compatibility due to legacy reasons
        return "93" if self == self.__class__.STD_1993 else str(self.value)

    @property
    def supports_context(self) -> bool:
        return self >= self.__class__.STD_2008

    @property
    def and_later(self) -> set[VHDLStandard]:
        """Selected and later standards."""
        return {s for s in self.__class__ if s >= self}

    @property
    def and_earlier(self) -> set[VHDLStandard]:
        """Selected and earlier standards."""
        return {s for s in self.__class__ if s <= self}

    @classmethod
    def standard(cls, year: str) -> VHDLStandard:
        """Resolve standard from 2 or 4 digit string."""
        # TODO: better name would be cls.from_string()
        short_form = {str(v)[-2:]: v for v in cls}
        return cls(short_form.get(year, year)) # type: ignore  # Throw a nice error


VHDL = VHDLStandard
