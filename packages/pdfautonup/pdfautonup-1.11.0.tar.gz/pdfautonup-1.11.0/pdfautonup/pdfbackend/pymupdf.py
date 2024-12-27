# Copyright Louis Paternault 2019-2024
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

"""Read and write PDF files using the PyMuPDF library."""

import contextlib
import decimal
import io
import sys

if sys.version_info >= (3, 11):
    try:
        import fitz_new as fitz
    except ImportError:
        import fitz
else:
    import fitz

# pylint: disable=wrong-import-position
from . import AbstractPDFFileReader, AbstractPDFFileWriter, AbstractPDFPage

VERSION = "pymupdf" + " ".join(fitz.version)


class PDFFileReader(AbstractPDFFileReader):
    """Read a PDF file."""

    def __init__(self, name=None):
        super().__init__()
        if name is None:
            # Read from standard input
            self._file = fitz.open(
                stream=io.BytesIO(sys.stdin.buffer.read()), filetype="application/pdf"
            )
        else:
            self._file = fitz.open(name)

    def close(self):
        self._file.close()

    def __len__(self):
        return self._file.page_count

    def __iter__(self):
        for page in self._file:
            yield PDFPage(page)

    def __getitem__(self, key):
        return self._file[key]

    @property
    def metadata(self):
        return self._file.metadata


class PDFFileWriter(AbstractPDFFileWriter):
    """PDF file writer."""

    def __init__(self):
        super().__init__()
        self._file = fitz.Document()

    @contextlib.contextmanager
    def new_page(self, width, height):
        yield PDFPage(self._file.new_page(width=width, height=height))

    def write(self, name=None):
        if name is None:
            sys.stdout.buffer.write(self._file.write())
        else:
            self._file.save(name)

    @property
    def metadata(self):
        return self._file.metadata

    @metadata.setter
    def metadata(self, value):
        self._file.set_metadata(value)


class PDFPage(AbstractPDFPage):
    """Page of a PDF file (using PyMuPDF)."""

    @property
    def parent(self):
        """PDF Object this page belongs to."""
        return self._page.parent

    @property
    def number(self):
        """Number of this page in the PDF."""
        return self._page.number

    @property
    def mediabox_size(self):
        """Return size of the mediabox, as a tuple of `(width, height)`."""
        return self._page.mediabox_size

    @property
    def rotated_size(self):
        if self._page.rotation % 180 == 0:
            return self._page.mediabox_size
        return (
            self._page.mediabox_size[1],
            self._page.mediabox_size[0],
        )

    def merge_translated_page(self, page, x, y):
        if (
            x + decimal.Decimal(page.mediabox_size.x) < 0
            or x > self.mediabox_size.x
            or y + decimal.Decimal(page.mediabox_size.y) < 0
            or y > self.mediabox_size.y
        ):
            # The merged page is drawn outside the current page (empty intersection).
            # Method show_pdf_page() does not like it, and raise an exception.
            return

        rotation = page.rotation
        page.set_rotation(0)
        if rotation % 180 == 0:
            width = page.mediabox_size[0]
            height = page.mediabox_size[1]
        else:
            width = page.mediabox_size[1]
            height = page.mediabox_size[0]

        self._page.show_pdf_page(
            fitz.Rect(
                x,
                decimal.Decimal(self.mediabox_size[1]) - y - decimal.Decimal(height),
                x + decimal.Decimal(width),
                decimal.Decimal(self.mediabox_size[1]) - y,
            ),
            page.parent,
            page.number,
            rotate=rotation,
        )
