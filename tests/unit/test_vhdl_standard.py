# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2014-2025, Lars Asplund lars.anders.asplund@gmail.com

"""
Test the vhdl_standard.py file
"""

from vunit.vhdl_standard import VHDLStandard


def test_valid_standards():
    for std in ["93", "02", "08", "19", "1993", "2002", "2008", "2019"]:
        VHDLStandard.resolve(std)


def test_error_on_invalid_standard():
    _assert_is_invalid("2001")
    _assert_is_invalid("002")
    _assert_is_invalid("993")
    _assert_is_invalid("2")
    _assert_is_invalid("3")


def test_equality():
    assert VHDLStandard.resolve("2008") == VHDLStandard.resolve("2008")
    assert VHDLStandard.resolve("1993") != VHDLStandard.resolve("2008")
    assert VHDLStandard.resolve("93") == VHDLStandard.resolve("1993")


def test_comparison():
    assert VHDLStandard.resolve("1993") < VHDLStandard.resolve("2002")
    assert VHDLStandard.resolve("2002") < VHDLStandard.resolve("2008")
    assert VHDLStandard.resolve("2008") < VHDLStandard.resolve("2019")


def test_str():
    assert str(VHDLStandard.resolve("1993")) == "93"
    assert str(VHDLStandard.resolve("2002")) == "2002"


def test_and_later():
    assert VHDLStandard.STD_1993.and_later == {
        VHDLStandard.STD_1993,
        VHDLStandard.STD_2002,
        VHDLStandard.STD_2008,
        VHDLStandard.STD_2019,
    }
    assert VHDLStandard.STD_2002.and_later == {
        VHDLStandard.STD_2002,
        VHDLStandard.STD_2008,
        VHDLStandard.STD_2019,
    }
    assert VHDLStandard.STD_2008.and_later == {VHDLStandard.STD_2008, VHDLStandard.STD_2019}
    assert VHDLStandard.STD_2019.and_later == {VHDLStandard.STD_2019}


def test_and_earlier():
    assert VHDLStandard.STD_2019.and_earlier == {
        VHDLStandard.STD_1993,
        VHDLStandard.STD_2002,
        VHDLStandard.STD_2008,
        VHDLStandard.STD_2019,
    }
    assert VHDLStandard.STD_2008.and_earlier == {VHDLStandard.STD_1993, VHDLStandard.STD_2002, VHDLStandard.STD_2008}
    assert VHDLStandard.STD_2002.and_earlier == {VHDLStandard.STD_1993, VHDLStandard.STD_2002}
    assert VHDLStandard.STD_1993.and_earlier == {VHDLStandard.STD_1993}


def test_supports_context():
    assert not VHDLStandard.STD_2002.supports_context
    assert VHDLStandard.STD_2008.supports_context


def _assert_is_invalid(standard_string):
    """
    Check that the standard string produces an exception
    """
    try:
        VHDLStandard.resolve(standard_string)
    except ValueError:
        pass
    else:
        raise AssertionError("Exception not raised")
