#!/usr/bin/env python3

# Copyright Louis Paternault 2014-2024
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

"""Main function for the command."""

import logging
import sys

from . import errors, options, pdfautonup, pdfbackend

LOGGER = logging.getLogger("pdfautonup")


def _progress_printer(string):
    """Returns a function that prints the progress message."""

    def print_progress(page, total):
        """Print progress message."""
        try:
            text = string.format(
                page=page, total=total, percent=int(page * 100 / total)
            )
        except:  # pylint: disable=bare-except
            text = string
        print(text, end="")
        sys.stdout.flush()

    return print_progress


def main():
    """Main function"""
    try:
        arguments = options.commandline_parser().parse_args(sys.argv[1:])

        if arguments.verbose:
            # pylint: disable=no-member
            sys.stderr.write(f"Using pdf backend {pdfbackend.get_backend().VERSION}\n")

        if "-" in arguments.files and arguments.interactive:
            LOGGER.error(
                """Cannot ask user input while reading files from standard input. """
                """Try removing the "--interactive" (or "-i") option."""
            )
            sys.exit(1)

        pdfautonup(
            arguments.files,
            arguments.output,
            arguments.target_size,
            algorithm=arguments.algorithm,
            repeat=arguments.repeat,
            interactive=arguments.interactive,
            orientation=arguments.orientation,
            progress=_progress_printer(arguments.progress),
            more={
                "gap": arguments.gap,
                "margin": arguments.margin,
            },
        )
        if not (arguments.progress.endswith("\n") or arguments.progress == ""):
            print()
    except KeyboardInterrupt:
        print()
        sys.exit(1)
    except errors.PdfautonupError as error:
        LOGGER.error(error)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
