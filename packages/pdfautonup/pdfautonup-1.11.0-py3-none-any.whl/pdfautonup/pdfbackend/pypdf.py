# Copyright Louis Paternault 2019-2023
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

"""Read and write PDF files using the PyPDF library."""

import contextlib
import io
import sys

import pypdf

from . import (
    METADATA_KEYS,
    AbstractPDFFileReader,
    AbstractPDFFileWriter,
    AbstractPDFPage,
)

VERSION = "pypdf" + pypdf.__version__


def _rectangle_size(rectangle):
    """Return the dimension of rectangle (width, height)."""
    return (
        rectangle.upper_right[0] - rectangle.lower_left[0],
        rectangle.upper_right[1] - rectangle.lower_left[1],
    )


def _metadata2dict(file):
    return {
        keyword: getattr(file.metadata, keyword)
        for keyword in METADATA_KEYS
        if (getattr(file.metadata, keyword, None) is not None)
    }


class PDFFileReader(AbstractPDFFileReader):
    """Read a PDF file."""

    def __init__(self, name=None):
        super().__init__()
        if name is None:
            # Read from standard input
            self._file = pypdf.PdfReader(io.BytesIO(sys.stdin.buffer.read()))
        else:
            self._file = pypdf.PdfReader(name)

    def close(self):
        pass

    def __len__(self):
        return len(self._file.pages)

    def __iter__(self):
        for page in self._file.pages:
            yield PDFPage(page)

    def __getitem__(self, key):
        return self._file.pages[key]

    @property
    def metadata(self):
        return _metadata2dict(self._file)


class PDFFileWriter(AbstractPDFFileWriter):
    """PDF file writer."""

    def __init__(self):
        super().__init__()
        self._file = pypdf.PdfWriter()

    @contextlib.contextmanager
    def new_page(self, width, height):
        yield PDFPage(self._file.add_blank_page(width=width, height=height))

    def write(self, name=None):
        if name is None:
            output = io.BytesIO()
            self._file.write(output)
            sys.stdout.buffer.write(output.getvalue())
        else:
            with open(name, "wb") as stream:
                self._file.write(stream)

    @property
    def metadata(self):
        return _metadata2dict(self._file)

    @metadata.setter
    def metadata(self, value):
        self._file.add_metadata(
            {f"/{keyword.capitalize()}": data for keyword, data in value.items()}
        )


class PDFPage(AbstractPDFPage):
    """Page of a PDF file (using pypdf)."""

    @property
    def rotated_size(self):
        size = _rectangle_size(self._page.mediabox)
        if self._page.rotation % 180 == 0:
            return size
        return (size[1], size[0])

    def merge_translated_page(self, page, x, y):
        # Handle rotated pages
        page.transfer_rotation_to_content()

        # Merge page
        self._page.merge_transformed_page(
            page, pypdf.Transformation().translate(float(x), float(y))
        )
