#!/usr/bin/env python3

# Copyright Louis Paternault 2011-2023
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>. 1

"""Generate dummy pdf files"""

import argparse
import logging
import random
import re
import sys
import textwrap

import papersize

from . import VERSION, errors
from .pdf import Page, generate, get_color

LOGGER = logging.getLogger("dummypdf")
LOGGER.addHandler(logging.StreamHandler())


def positive_int(arg):
    """Return a positive argument corresponding to ``arg``."""
    try:
        number = int(arg)
    except ValueError as error:
        raise argparse.ArgumentTypeError(arg) from error
    if number < 0:
        raise argparse.ArgumentTypeError(arg)
    return number


def filename(extension=None):
    """Return the filename.

    - If no argument is provided, return the bare file name.
    - If an argument is provided, it is the extension of the file to be
      returned.
    """

    if extension is None:
        return "dummy"
    return f"dummy.{extension}"


def type_papersize(text):
    """Parse 'text' as the argument of --papersize.

    Return a tuple of :class:`float`.
    """
    try:
        return tuple(map(float, papersize.parse_papersize(text)))
    except papersize.PapersizeException as error:
        raise argparse.ArgumentTypeError(str(error))


def type_rotate(text):
    """Parse 'text' as the argument of --orientation.

    Return an integer, multiple of 90.
    """
    try:
        angle = int(text)
    except ValueError as error:
        raise argparse.ArgumentTypeError(str(error)) from error
    if angle % 90 == 0:
        return angle % 360
    raise argparse.ArgumentTypeError("Argument of --rotation must be a multiple of 90.")


RE_FORMAT = re.compile(
    r"""(
            (?P<count>\d+)
            |
            (?P<orientation>(L(andscape)?)|(P(ortrait)?))
            |
            (?P<rotation>(N(orth)?)|(S(outh)?)|(E(east)?)|(W(est)?))
        ){,3}
        """,
    re.IGNORECASE | re.VERBOSE,
)

ROTATION2ANGLE = {
    "north": 0,
    "east": 90,
    "south": 180,
    "west": 270,
}


def rotation2angle(rotation):
    """Convert a string ("north", "south", etc. or their first letter) to an angle."""
    if rotation is None:
        return 0
    for key, value in ROTATION2ANGLE.items():
        if rotation.lower() == key or key.startswith(rotation.lower()):
            return value
    raise KeyError()


ORIENTATION = ("landscape", "portrait")


def orientation2string(orientation):
    """Convert a string  to full words "portrait" or "landscape".

    The argument must be "portrait" or "landscape", or their initial.
    """
    if orientation is None:
        return None
    for candidate in ORIENTATION:
        if orientation.lower() == candidate or candidate.startswith(
            orientation.lower()
        ):
            return candidate
    raise KeyError()


def type_papersize_list(text):
    """Parse 'text' as one of the positional arguments.

    That is, either a papersize (e.g. "a4"), or a papersize and a page count,
    separated by a colon (e.g. "a4:3").
    """
    try:
        if text.count(":") == 0:
            return (papersize.parse_papersize(text), 0, None, 1)
        if text.count(":") == 1:
            paper, pageformat = text.split(":")
            if match := RE_FORMAT.fullmatch(pageformat):
                groups = match.groupdict()
            else:
                raise argparse.ArgumentTypeError(
                    f"Invalid page format: '{pageformat}'."
                )
            return (
                papersize.parse_papersize(paper),  # Paper size
                rotation2angle(groups["rotation"]),  # Rotation
                orientation2string(groups["orientation"]),  # Orientation
                (
                    int(groups["count"]) if groups["count"] is not None else 1
                ),  # Number of such pages
            )
        raise argparse.ArgumentTypeError(
            f"Argument '{text}' must be PAPERSIZE or PAPERSIZE:PAGECOUNT."
        )
    except papersize.PapersizeException as error:
        raise argparse.ArgumentTypeError(f"Paper size error: {error}") from error


class ListColors(argparse.Action):
    """Argparse action to list available named colors."""

    #: pylint: disable=too-few-public-methods

    def __init__(self, *args, **kwargs):
        if "nargs" in kwargs:
            raise ValueError("nargs not allowed")
        kwargs["nargs"] = 0
        super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        # pylint: disable=signature-differs
        print(" ".join(get_color()))
        sys.exit(0)


def commandline_parser():
    """Return a command line parser."""

    parser = argparse.ArgumentParser(
        prog="dummypdf",
        description="Generate dummy PDF",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=textwrap.dedent(
            # pylint: disable=line-too-long
            """
            One can use either positional arguments (`dummypdf A4:2`) or explicit arguments (`dummypdf --paper A4 --number 2`).
            If the pages of the output PDF have different size, orientation, or rotation, only positional arguments can be used.
            """
        ),
    )

    parser.add_argument(
        "--version",
        help="Show version",
        action="version",
        version="%(prog)s " + VERSION,
    )

    parser.add_argument(
        "--output",
        "-o",
        default=filename("pdf"),
        help=textwrap.dedent(
            """
            Output file.
            Default is "dummy.pdf". Use "--output=-" to pipe data to standard output.
        """
        ),
        type=str,
    )

    parser.add_argument(
        "--number",
        "-n",
        help=textwrap.dedent(
            """
        Number of pages. Can be 0 to generate a file with no pages.
        Incompatible with positional arguments.
        """
        ),
        type=positive_int,
    )

    parser.add_argument(
        "--orientation",
        "-O",
        help="Paper orientation. Default depends on the paper size.",
        default=None,
        choices=["portrait", "landscape"],
    )

    parser.add_argument(
        "--start", "-s", help="Number of first page.", default=1, type=int
    )

    parser.add_argument(
        "--papersize",
        "-p",
        type=type_papersize,
        help=textwrap.dedent(
            """
        Paper size, as either a named size (e.g. "A4" or "letter"), or a couple
        of lengths (e.g. "21cmx29.7cm" or "7in 8in"…). Default value is A4.
        Incompatible with positional arguments.
        """
        ),
    )

    parser.add_argument(
        "--rotation",
        "-r",
        help="Paper rotation, in degrees.",
        default=None,
        type=type_rotate,
    )

    parser.add_argument(
        "list",
        type=type_papersize_list,
        help=textwrap.dedent(
            # pylint: disable=line-too-long
            """
        List of paper size and page format (optional), separated by a colon.
        - The paper size format is the same as the argument of `--papersize`.
        - The page format is case insensitive and can contain any of:
            - a positive integer (possibly zero): the number of such pages;
            - an orientation: portrait or landscape (or their first letter p or l);
            - a rotation: north, south, east, west (or their first letter n, s, e, w).
        For instance, "a4 a5:2 10cmx100mm:landscape3west" will produce a file with one a4 page, two a5 pages, and three landscape, rotated west, 10cmx100mm pages.

        Those positional arguments are incompatible with options `--papersize`, `--orientation`, `--rotation`, and `--number`.
        """
        ),
        nargs="*",
    )

    parser.add_argument(
        "--color",
        "-c",
        default="deterministic",
        help=textwrap.dedent(
            """
        Color to use. Can be:

        - deterministic (default): a random color is used, but calls to
          dummypdf using the same arguments give the same color (note that
          calls with different version of this program may lead to different
          colors used).
        - random: a random color is used (different on each call).
        - RED,GREEN,BLUE: a RGB color, where RED, GREEN and BLUE are integers
          between 0 and 255.
        - named colors: Run "dummypdf --list-colors" for the list of available color names.
        """
        ),
    )

    parser.add_argument(
        "--list-colors",
        help='List named colors (to be used with option "--color") and exits.',
        action=ListColors,
    )

    return parser


def pageiterator(options):
    """Iterate over pages to be produced.

    - Argument: The namespace of options (as produced by :mod:`argparse`).
    - Return: An iterator of pages, as :class:`dummypdf.pdf.Page` objects.
    """
    if options.list:
        if (
            (options.number is not None)
            or (options.papersize is not None)
            or (options.orientation is not None)
            or (options.rotation is not None)
        ):
            raise errors.DummypdfError(
                # pylint: disable=line-too-long
                "Options '--number', '--papersize', '--orientation', '--rotation' are incompatible with positional arguments."
            )
        for pageformat in options.list:
            size, rotation, orientation, count = pageformat
            for _ in range(count):
                yield Page(
                    size=tuple(map(float, size)),
                    orientation=orientation,
                    rotation=rotation,
                )
    else:
        if options.papersize is None:
            options.papersize = tuple(map(float, papersize.parse_papersize("a4")))
        if options.number is None:
            options.number = 1
        for _ in range(options.number):
            yield Page(
                size=options.papersize,
                rotation=options.rotation,
                orientation=options.orientation,
            )


RE_COLOR = re.compile(r"(?P<red>\w+),(?P<green>\w+),(?P<blue>\w+)")


def process_color(options):
    """Compute the color."""
    if options.color.lower() in ["deterministic", "random"]:
        if options.color.lower() == "deterministic":
            random.seed(
                # pylint: disable=line-too-long
                f"{options.start}-{options.number}-{options.papersize}-{options.orientation}-{options.rotation}-{options.list}"
            )
        return random.sample(
            (
                random.randint(64, 255),
                random.randint(0, 191),
                random.randint(0, 255),
            ),
            k=3,
        )
    if RE_COLOR.match(options.color):
        color = [
            int(component) for component in RE_COLOR.match(options.component).groups()
        ]
        for component in color:
            if component > 255:
                raise errors.ArgumentError(
                    "Option '--color' must be an integer between 0 and 255."
                )
        return color
    return get_color(options.color)


def main():
    """Main function"""

    try:
        options = commandline_parser().parse_args()
        generate(
            name=options.output,
            first=options.start,
            color=process_color(options),
            pages=pageiterator(options),
        )

    except errors.DummypdfError as error:
        LOGGER.error(error)
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(1)


if __name__ == "__main__":
    main()
