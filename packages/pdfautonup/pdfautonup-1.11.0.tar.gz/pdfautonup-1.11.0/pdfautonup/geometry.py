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

"""Different algorithm to fit source files into destination files."""

import contextlib
import logging
import operator
import os
from collections import namedtuple
from decimal import Decimal, DivisionByZero

import papersize

from . import errors, paper, pdfbackend

LOGGER = logging.getLogger("pdfautonup")


def _dist_to_round(x):
    """Return distance of ``x`` to ``round(x)``."""
    return abs(x - round(x))


class _Layout:
    def __init__(self, target_size, **arguments):
        self.target_size = target_size
        self.interactive = arguments.get("interactive", False)

        self.pdf = pdfbackend.get_backend().PDFFileWriter()

    @contextlib.contextmanager
    def new_page(self):
        """Context manager to return a new, blank page.

        The page is expected to stay unchanged after the ``__exit__()`` method.
        """
        with self.pdf.new_page(
            width=round(self.target_size[0]), height=round(self.target_size[1])
        ) as new_page:
            yield new_page

    def add_page(self, sourcepage, destpage, number):
        """Add ``page`` to the destination file.

        It is added at the right place for `number`:
        if `N` source pages can fit into *one* destination page,
        then `number` is an integer from `0` to `N-1`.
        """
        (x, y) = self.cell_bottomleft(number)
        destpage.merge_translated_page(sourcepage, x, y)

    def write(self, outputname, inputname, *, metadata):
        """Write destination file."""
        # I wonder whether this functions should be moved in another module, or
        # not: it is the only function dealing with file system in this module.
        self._set_metadata(metadata)

        if outputname is None and inputname == "-":
            outputname = "-"
        elif outputname is None:
            outputname = f"""{inputname[: -len(".pdf")]}-nup.pdf"""

        if outputname != "-" and self.interactive and os.path.exists(outputname):
            question = f"File {outputname} already exists. Overwrite (y/[n])? "
            if input(question).lower() != "y":
                raise errors.PdfautonupError("Cancelled by user.")

        if outputname == "-":
            self.pdf.write()
        else:
            self.pdf.write(outputname)

    def _set_metadata(self, metadata):
        """Set metadata on current pdf."""
        metadata["producer"] = (
            "pdfautonup, using the PyPDF library — http://framagit.org/spalax/pdfautonup"
        )
        self.pdf.metadata = metadata

    def cell_bottomleft(self, num):
        """Return the bottom left coordinate of ``num``th cell of page."""
        raise NotImplementedError()

    @property
    def pages_per_page(self):
        """Return the number of source pages per destination page."""
        raise NotImplementedError()


class Fuzzy(_Layout):
    """Documents can overlap, and space can be wasted, but not too much."""

    #: A target size, associated with the number of source pages that will fit
    #: in it, per width and height (``cell_number[0]`` and ``cell_number[1]``).
    Grid = namedtuple("Grid", ["cell_number", "target_size", "margins", "gaps"])

    def __init__(self, source_size, target_size, **arguments):
        if (
            arguments["more"].get("margin", None) is not None
            or arguments["more"].get("gap", None) is not None
        ):
            LOGGER.warning(
                "Arguments `--margin` and `--gap` are ignored with algorithm `fuzzy`."
            )
        self.source_size = source_size
        if arguments["orientation"] == "landscape":
            self.grid = self.generate_grid(
                source_size, papersize.rotate(target_size, papersize.LANDSCAPE)
            )
        elif arguments["orientation"] == "portrait":
            self.grid = self.generate_grid(
                source_size, papersize.rotate(target_size, papersize.PORTRAIT)
            )
        else:
            self.grid = min(
                self.generate_grid(source_size, target_size),
                self.generate_grid(source_size, (target_size[1], target_size[0])),
                key=self.ugliness,
            )

        super().__init__(self.grid.target_size, **arguments)

    def ugliness(self, grid):
        """Return the "ugliness" of this ``grid``.

        - A layout that fits perfectly has an ugliness of 0.
        - The maximum ugliness is 1.
        """
        target_width, target_height = grid.target_size
        source_width, source_height = self.source_size
        return (
            _dist_to_round(target_width / source_width) ** 2
            + _dist_to_round(target_height / source_height) ** 2
        )

    @staticmethod
    def _margins(target_size, source_size, cell_number):
        if cell_number[0] == 1:
            width = (target_size[0] - source_size[0] * cell_number[0]) / 2
        else:
            width = 0
        if cell_number[1] == 1:
            height = (target_size[1] - source_size[1] * cell_number[1]) / 2
        else:
            height = 0
        return [width, height]

    @staticmethod
    def _gaps(target_size, source_size, cell_number):
        if cell_number[0] == 1:
            width = Decimal(0)
        else:
            width = (target_size[0] - cell_number[0] * source_size[0]) / (
                cell_number[0] - 1
            )
        if cell_number[1] == 1:
            height = Decimal(0)
        else:
            height = (target_size[1] - cell_number[1] * source_size[1]) / (
                cell_number[1] - 1
            )
        return (width, height)

    def generate_grid(self, source_size, target_size):
        """Return a :class:`self.Grid` object for arguments.

        The main function is computing the number of source pages per
        destination pages.
        """
        try:
            cell_number = (
                max(1, round(target_size[0] / source_size[0])),
                max(1, round(target_size[1] / source_size[1])),
            )
        except DivisionByZero as error:
            raise errors.PdfautonupError(
                "Error: A PDF page have a null dimension."
            ) from error
        return self.Grid(
            cell_number,
            target_size,
            self._margins(target_size, source_size, cell_number),
            self._gaps(target_size, source_size, cell_number),
        )

    def cell_bottomleft(self, num):
        # pylint: disable=line-too-long
        width, _height = self.grid.cell_number
        return (
            self.grid.margins[0]
            + (self.source_size[0] + self.grid.gaps[0]) * (num % width),
            self.grid.margins[1]
            + (self.source_size[1] + self.grid.gaps[1]) * (num // width),
        )

    @property
    def pages_per_page(self):
        return self.grid.cell_number[0] * self.grid.cell_number[1]


class Panelize(_Layout):
    """Minimum margin is defined, as well as fixed gap."""

    #: Define how the source page will fit into the destination page.
    #: - `margin` is the destination margin of the bottom left corner
    #:   (including wasted space), as a tuple: (left, bottom).
    #: - `sourcex` is the 'extended' source size (source size, together with gap).
    Grid = namedtuple(
        "Grid", ["margin", "sourcex", "dimension", "target", "pagenumber"]
    )

    def __init__(self, source_size, target_size, **arguments):
        # pylint: disable=too-many-arguments
        self.gap = arguments["more"].get("gap", papersize.parse_length("0"))
        if self.gap is None:
            self.gap = papersize.parse_length("0")
        elif isinstance(self.gap, str):
            self.gap = papersize.parse_length(self.gap)

        self.margin = paper.Margins.parse(arguments["more"].get("margin", None))

        if arguments["orientation"] == "landscape":
            self.grid = self.generate_grid(
                source_size,
                papersize.rotate(target_size, papersize.LANDSCAPE),
                self.margin,
            )
        elif arguments["orientation"] == "portrait":
            self.grid = self.generate_grid(
                source_size,
                papersize.rotate(target_size, papersize.PORTRAIT),
                self.margin,
            )
        else:
            self.grid = max(
                self.generate_grid(source_size, target_size, self.margin),
                self.generate_grid(
                    source_size, (target_size[1], target_size[0]), self.margin
                ),
                key=operator.attrgetter("pagenumber"),
            )

        if self.pages_per_page == 0:
            raise errors.PdfautonupError(
                "Error: Format constraints too tight: Cannot fit any"
                "source page into destination page."
            )

        super().__init__(self.grid.target, **arguments)

    def generate_grid(
        self,
        source: tuple[Decimal, Decimal],
        target: tuple[Decimal, Decimal],
        margin: paper.Margins,
    ) -> "Panelize.Grid":
        """Computes the geometry of the output file.

        It computes how many source pages will be merged on each destination pages,
        the total number of pages, the margins, etc.
        """

        dimension = (
            self._num_fit(target[0], margin.left + margin.right, source[0]),
            self._num_fit(target[1], margin.top + margin.bottom, source[1]),
        )

        wasted = (
            self._wasted(
                target[0], margin.left + margin.right, dimension[0], source[0]
            ),
            self._wasted(
                target[1], margin.top + margin.bottom, dimension[1], source[1]
            ),
        )
        return self.Grid(
            margin=(margin.left + wasted[0], margin.bottom + wasted[1]),
            sourcex=(source[0] + self.gap, source[1] + self.gap),
            dimension=dimension,
            target=target,
            pagenumber=dimension[0] * dimension[1],
        )

    def _wasted(self, dest, margins, num, source):
        """Return the amount of wasted space

        When fitting `num` elements of size `source` into element of size
        `dest` (in one dimension).

        `margins` is the total margin in the beginning and the end of this dimension.
        """
        return (dest - num * (source + self.gap) - margins + self.gap) / 2

    def _num_fit(self, target, margins, source):
        """Return the number of source elements that can fit in target.

        `source`, `target` and `margins` are all sizes, in one dimension.

        `margins` is the total margin in the beginning and the end of this dimension.
        """
        return int((target - margins + self.gap) // (source + self.gap))

    @property
    def pages_per_page(self):
        return self.grid.dimension[0] * self.grid.dimension[1]

    def cell_bottomleft(self, num):
        width, _height = self.grid.dimension
        return (
            self.grid.margin[0] + self.grid.sourcex[0] * (num % width),
            self.grid.margin[1] + self.grid.sourcex[1] * (num // width),
        )
