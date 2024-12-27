# Copyright 2014-2024 Louis Paternault and contributors

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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Convert PDF files to 'n-up' PDF files, guessing the output layout.

"""

import collections
import decimal
import logging
import math
from collections.abc import Callable, Sequence
from typing import Literal

from . import errors, geometry, paper, pdfbackend

VERSION = "1.11.0"
__AUTHOR__ = "Louis Paternault (spalax@gresille.org)"
__COPYRIGHT__ = "(C) 2014-2024 Louis Paternault. GNU AGPL 3 or later."

LOGGER = logging.getLogger("pdfautonup")


def _none_function(*args, **kwargs):  # pylint: disable=unused-argument
    """Accept any number of arguments. and does nothing."""


class _PageSequence(collections.abc.Sequence):
    """Sequence of pages of several PDF files."""

    def __init__(self, filenames):
        self.files = []
        self._filenames = filenames

    def __enter__(self):
        for name in self._filenames:
            try:
                if name == "-":
                    self.files.append(pdfbackend.get_backend().PDFFileReader())
                else:
                    self.files.append(pdfbackend.get_backend().PDFFileReader(name))
            except (FileNotFoundError, PermissionError) as error:
                raise errors.PdfautonupError(
                    f"Error while reading file '{name}': {error}."
                )
            except RuntimeError as error:
                raise errors.PdfautonupError(
                    f"Error: Malformed file '{name}': {error}."
                )
        return self

    def __exit__(self, *exc):
        for file in self.files:
            file.close()

    def __iter__(self):
        for pdf in self.files:
            yield from pdf

    def __len__(self):
        return sum(len(pdf) for pdf in self.files)

    def __getitem__(self, index):
        for file in self.files:
            try:
                return file[index]
            except IndexError:
                index -= len(file)
        raise IndexError

    def metadata(self):
        """Aggregate metadata from input files."""
        if len(self.files) == 1:
            return self.files[0].metadata

        input_info = [pdf.metadata for pdf in self.files]
        output_info = {}
        for key in pdfbackend.METADATA_KEYS:
            values = list(
                data[key]
                for data in input_info
                if (key in data and (data[key] is not None))
            )
            if values:
                output_info[key] = " / ".join([f"“{item}”" for item in values])
        return output_info


def pdfautonup(
    files: Sequence[str],
    output: str = None,
    size: str | None | tuple[decimal.Decimal] = None,
    *,
    algorithm: Literal["fuzzy", "panel"] | None = None,
    repeat: Literal["auto", "fit"] | int = "auto",
    more: dict = None,
    interactive: bool = False,
    orientation: Literal["auto", "portrait", "landscape"] = "auto",
    progress: Callable[[int, int], None] = _none_function,
):  # pylint: disable=too-many-arguments, too-many-locals
    """Convert PDF files to 'n-up' PDF files, guessing the output layout.

    .. versionadded:: 1.9.0

    :param files: Names of the files to process.
    :param output: Name of the output file. If ``None``, writes to standard output.
    :param size: Size of the pages of the destination file, either as:
        a tuple of :class:`decimal.Decimal` (width and height, in points);
        a string to be parsed by :func:`papersize.parse_papersize`;
        :class:`None`, in which case the default paper size will be used.
    :param repeat: If a number, repeat the input file this number of times.
        If ``"fit"``, repeat the input files as many times as necessary to fill
        all pages of the destination file. If ``"auto"``, is equivalent to
        ``"fit"`` if input file has one page, and equivalent to ``1``
        otherwise.
    :param algorithm: Select one algorithm, either ``"fuzzy"`` (document pages
        can overlap or leave blank space between them, but not too much) or
        ``"panel"`` (the gap length between source pages is fixed, and a
        minimum destination margin is respected). If ``None``, chooses
        ``"panel"`` if ``"margin"`` or ``"gap"`` are defined in ``more``, and
        ``"fuzzy"`` otherwise.
    :param orientation: Force orientation of destination file to portrait or landscape.
        If ``"auto"``, select the one that fits the most input pages.
    :param more: Additional arguments for algorithms.
        The *fuzzy* algorithm does not accept any arguments, while the *panel*
        algorithm accepts ``"margin"`` and ``"gap"`` (as strings
        to parsed by :func:`papersize.parse_length` or :class:`decimal.Decimal`
        as the length in points).
        ``"margin"`` may also be a 2- to 4-tuple to specify individual margins
        in the same order and arity as in CSS.
    :param progress: A function that takes to integer arguments
        (number of pages processed so far, and total number of pages to
        process), and display a progress. Whether it is displayed on standard
        input or a GUI or something else is up to you.
    :param interactive: If ``True``, asks for confirmation before overwriting
        the destination file, if it already exists.


    .. warning::

       If a file is ``"-"``, it is read from standard input.
       I am still undecided about how reading from standard input should be
       handled, so this might change in the future.

       So, right now, reading from standard input is unsupported, and input
       files cannot be named ``"-"``.
    """
    # pylint: disable=too-many-branches

    with _PageSequence(files) as pages:
        if not pages:
            raise errors.PdfautonupError("Error: PDF files have no pages to process.")

        page_sizes = list(zip(*[page.rotated_size for page in pages]))
        source_size = (
            decimal.Decimal(max(page_sizes[0])),
            decimal.Decimal(max(page_sizes[1])),
        )
        target_size = paper.target_papersize(size)

        if [len(set(page_sizes[i])) for i in (0, 1)] != [1, 1]:
            LOGGER.warning(
                "Pages have different sizes. The result might be unexpected."
            )

        if more is None:
            more = {}
        if algorithm is None:
            if more.get("gap", None) is None and more.get("margin", None) is None:
                fit = geometry.Fuzzy
            else:
                fit = geometry.Panelize
        else:
            fit = {"fuzzy": geometry.Fuzzy, "panel": geometry.Panelize}[algorithm]

        dest = fit(
            source_size,
            target_size,
            orientation=orientation,
            interactive=interactive,
            more=more,
        )

        if repeat == "auto":
            if len(pages) == 1:
                repeat = "fit"
            else:
                repeat = 1
        if repeat == "fit":
            repeat = math.lcm(dest.pages_per_page, len(pages)) // len(pages)

        totalpages = repeat * len(pages)
        progress(0, totalpages)
        for destcount in range(math.ceil(totalpages / dest.pages_per_page)):
            with dest.new_page() as destpage:
                for sourcecount in range(
                    destcount * dest.pages_per_page,
                    (destcount + 1) * dest.pages_per_page,
                ):
                    if sourcecount < totalpages:
                        dest.add_page(
                            pages[sourcecount % len(pages)],
                            destpage,
                            sourcecount % dest.pages_per_page,
                        )
                        progress(sourcecount + 1, totalpages)

        dest.write(output, files[0], metadata=pages.metadata())
