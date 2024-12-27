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

"""PDF generation."""

import dataclasses
import sys

import papersize
from reportlab.lib import colors
from reportlab.pdfgen import canvas

from . import errors

LINEWIDTH = 5

# Very very approximate size of a "Times-Roman" digit, in font 1
CHARWIDTH = 0.497_923_228
CHARHEIGHT = 0.704_205_709


@dataclasses.dataclass
class Page:
    """A page, with a size and a rotation."""

    size: tuple
    rotation: int = 0
    orientation: dataclasses.InitVar[str] = None

    def __post_init__(self, orientation):
        if self.size == (0, 0):
            raise errors.DummypdfError(
                "Error: I cannot produce pages with dimension 0x0."
            )
        if self.size[0] < 0 or self.size[1] < 0:
            raise errors.DummypdfError(
                f"Error: I cannot produce pages with negative dimension: '{self.size}'."
            )
        if orientation is not None:
            self.size = tuple(
                sorted(
                    (float(self.size[0]), float(self.size[1])),
                    reverse=(orientation == "landscape"),
                )
            )
        if self.rotation is None:
            self.rotation = 0


def shift(coordinate):
    """Shift line coordinate.

    If we do not do that, half of lines are printed outside the page.
    """
    if coordinate == 0:
        return LINEWIDTH // 2
    return coordinate - LINEWIDTH // 2


def fontsize(pagenumber, paperwidth, paperheight):
    """Return the font size to be used to display page numbers."""
    if papersize.is_portrait(paperwidth, paperheight):
        size = int(paperheight / (3 * CHARHEIGHT))
    else:
        size = int(paperheight / (2 * CHARHEIGHT))
    charnumber = max(0, len(str(pagenumber)))
    if charnumber * CHARWIDTH * size > 0.9 * paperwidth:
        size = int(0.9 * paperwidth / (charnumber * CHARWIDTH))
    return size


def generate(name, first, color, pages):
    """Generate the pdf.

    Arguments:
    - name: file name (or "-" to write to standard output)
    - first: number of first page
    - color: line colors, as a list of three colors (RGB, from 0 to 255) or a
      named color recognisez by reportlab.
    - list of pages, as :class:`Page` objects.
    """
    # pylint: disable=too-many-locals
    if name == "-":
        name = sys.stdout.buffer
    pdf = canvas.Canvas(name)

    if isinstance(color, list):
        red, green, blue = color

        def set_line_color():
            """Set color of lines, using RGB color"""
            pdf.setFillColorRGB(red / 255, green / 255, blue / 255)
            pdf.setStrokeColorRGB(red / 255, green / 255, blue / 255)

    elif isinstance(color, str):

        def set_line_color():
            """Set color of lines, using named color"""
            pdf.setFillColor(getattr(colors, color))
            pdf.setStrokeColor(getattr(colors, color))

    pagenumber = first
    for page in pages:
        # Set page size
        pagewidth, pageheight = page.size
        if page.rotation % 180 == 0:
            pdf.setPageSize((pagewidth, pageheight))
        else:
            pdf.setPageSize((pageheight, pagewidth))
        pdf.setPageRotation(page.rotation)

        # Draw lines
        set_line_color()
        pdf.setLineWidth(LINEWIDTH)
        for x1, y1, x2, y2 in [  # pylint: disable=invalid-name
            (0, 0, pagewidth, 0),
            (pagewidth, 0, pagewidth, pageheight),
            (pagewidth, pageheight, 0, pageheight),
            (0, pageheight, 0, 0),
        ]:
            pdf.line(shift(x1), shift(y1), shift(x2), shift(y2))
        pdf.line(pagewidth, pageheight, 0, 0)
        pdf.line(pagewidth, 0, 0, pageheight)

        # Drawing text
        pdf.setFont("Times-Roman", fontsize(pagenumber, pagewidth, pageheight))
        pdf.setFillColor(colors.lightgrey)
        pdf.drawCentredString(
            float(pagewidth // 2),
            float(pageheight // 2 - 0.33 * fontsize(pagenumber, pagewidth, pageheight)),
            str(pagenumber),
        )

        # Next page
        pagenumber += 1
        pdf.showPage()

    pdf.setAuthor("Generated using dummypdf — http://framagit.org/spalax/dummypdf")
    pdf.setTitle("Dummy pdf")
    pdf.save()


def get_color(name=None):
    """Return color names.

    If name is None, return the list of available colors (as strings).
    If name is a string, return the string if this color exists; raises an
    error otherwise.
    """
    available = [
        color
        for color in dir(colors)
        if isinstance(getattr(colors, color), colors.Color)
    ]
    if name is None:
        return available
    if name in available:
        return name
    raise errors.ArgumentError(
        f"No such color '{name}'. See help for the list of available colors."
    )
