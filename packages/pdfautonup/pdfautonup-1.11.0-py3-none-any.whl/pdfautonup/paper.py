# Copyright 2014-2024 Louis Paternault and contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Paper-size related functions"""

import os
import subprocess
import typing
from decimal import Decimal

import papersize

from . import errors


def parse_lc_paper(string) -> tuple[Decimal, Decimal]:
    """Parse LC_PAPER locale variable

    We assume units are milimeters.
    """
    dimensions = {}
    for line in string.split("\n"):
        if line.startswith("width="):
            dimensions["width"] = papersize.parse_length(f"{line[6:]}mm")
        if line.startswith("height="):
            dimensions["height"] = papersize.parse_length(f"{line[7:]}mm")
    if len(dimensions) == 2:
        return (dimensions["width"], dimensions["height"])
    raise errors.CouldNotParse(string)


def target_papersize(target_size) -> tuple[Decimal, Decimal]:
    """Return the target paper size.

    :param str|tuple[decimal.Decimal]|None target_size: Target size,
        if provided by user in command line.
    """
    # pylint: disable=too-many-return-statements

    # Option set by user on command line
    if target_size is not None:
        if isinstance(target_size, str):
            return papersize.parse_papersize(target_size)
        return target_size

    # LC_PAPER environment variable (can be read from "locale -k LC_PAPER"
    try:
        return parse_lc_paper(
            subprocess.check_output(["locale", "-k", "LC_PAPER"], text=True)
        )
    except (FileNotFoundError, subprocess.CalledProcessError, errors.CouldNotParse):
        pass

    # PAPERSIZE environment variable
    try:
        return papersize.parse_papersize(os.environ["PAPERSIZE"].strip())
    except KeyError:
        pass

    # file described by the PAPERCONF environment variable
    try:
        return papersize.parse_papersize(
            # pylint: disable=unspecified-encoding
            open(os.environ["PAPERCONF"])
            .read()
            .strip()
        )
    except errors.CouldNotParse:
        raise
    except:  # pylint: disable=bare-except
        pass

    # content of /etc/papersize
    try:
        # pylint: disable=unspecified-encoding
        return papersize.parse_papersize(open("/etc/papersize").read().strip())
    except errors.CouldNotParse:
        raise
    except:  # pylint: disable=bare-except
        pass

    # stdout of the paperconf command
    try:
        return papersize.parse_papersize(
            subprocess.check_output(["paperconf"], text=True).strip()
        )
    except (FileNotFoundError, subprocess.CalledProcessError, errors.CouldNotParse):
        pass

    # Eventually, if everything else has failed, a4
    return papersize.parse_papersize("a4")


class Margins(typing.NamedTuple):
    """Represents the margins at all four sides of a page."""

    top: Decimal
    right: Decimal
    bottom: Decimal
    left: Decimal

    @classmethod
    def parse(
        cls,
        margin: "None | str | Decimal | typing.Sequence[str | Decimal] | typing.Self",
    ) -> "typing.Self":
        """Normalize a margin specification into a (top, right, bottom, left) quadruple
        and parse any strings into numbers.
        """
        match margin:
            case Margins(top, right, bottom, left):
                pass
            case None:
                return cls.parse(papersize.parse_length(string="0"))
            case str(margin):
                return cls.parse((papersize.parse_length(margin),))
            case Decimal() as margin:
                return cls.parse((margin,))
            case [*margins]:  # "sequence" pattern despite square-brackets
                match tuple(
                    papersize.parse_length(m) if not isinstance(m, Decimal) else m
                    for m in margins
                ):
                    case (all_four_sides,):
                        top = right = bottom = left = all_four_sides
                    case (
                        vertical,
                        horizontal,
                    ):
                        top = bottom = vertical
                        right = left = horizontal
                    case (
                        top,
                        horizontal,
                        bottom,
                    ):
                        left = right = horizontal
                    case (
                        top,
                        right,
                        bottom,
                        left,
                    ):
                        pass
                    case _:
                        return cls.parse(papersize.parse_length(string="0"))
        return cls(top, right, bottom, left)
