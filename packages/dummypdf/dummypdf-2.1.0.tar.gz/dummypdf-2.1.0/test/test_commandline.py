# Copyright 2017-2023 Louis Paternault
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Tests"""

import os
import subprocess
import sys
import unittest

from wand.image import Image

if "COVERAGE_PROCESS_START" in os.environ:
    EXECUTABLE = ["coverage", "run"]
else:
    EXECUTABLE = [sys.executable]

if sys.version_info < (3, 9):
    import pathlib

    import pkg_resources

    TEST_DATA_DIR = pathlib.Path(
        pkg_resources.resource_filename(__name__, "test_commandline-data")
    )
else:
    import importlib.resources

    TEST_DATA_DIR = importlib.resources.files("test") / "test_commandline-data"

FIXTURES = [
    # pylint: disable=line-too-long
    # {
    #    "remove": ("dummy.pdf",),
    #    "command": ["-n", "0", "-p", "a4"],
    #    "returncode": 0,
    #    "diff": ("dummy.pdf", TEST_DATA_DIR / "zero.pdf"),
    # },
    # {
    #    "remove": ("dummy.pdf",),
    #    "command": ["--papersize", "0cmx1cm"],
    #    "returncode": 0,
    #    "diff": ("dummy.pdf", TEST_DATA_DIR / "null.pdf"),
    # },
    {
        "remove": ("dummy.pdf",),
        "command": ["-n", "10", "--start", "20", "--papersize", "10cmx100mm"],
        "returncode": 0,
        "diff": ("dummy.pdf", TEST_DATA_DIR / "twenty.pdf"),
    },
    {
        "remove": ("dummy.pdf",),
        "command": [],
        "returncode": 0,
        "diff": ("dummy.pdf", TEST_DATA_DIR / "default.pdf"),
    },
    {
        "remove": ("dummy.pdf",),
        "command": ["--rotation", "90"],
        "returncode": 0,
        "diff": ("dummy.pdf", TEST_DATA_DIR / "rotation90.pdf"),
    },
    {
        "remove": ("dummy.pdf",),
        "command": ["a4", "a5:2", "a6:0", "10cmx100mm", "10cmx100mm"],
        "returncode": 0,
        "diff": ("dummy.pdf", TEST_DATA_DIR / "positional1.pdf"),
    },
    {
        "remove": ("dummy.pdf",),
        "command": ["A4", "A4:", "A5:landscape", "A5:south", "A6:lw3", "A7:2landscape"],
        "returncode": 0,
        "diff": ("dummy.pdf", TEST_DATA_DIR / "positional2.pdf"),
    },
    # Errors
    {
        "command": ["-n", "1", "a4"],
        "returncode": 1,
        "stderr": "Options '--number', '--papersize', '--orientation', '--rotation' are incompatible with positional arguments.\n",
    },
    {
        "command": ["-p", "a4", "a4"],
        "returncode": 1,
        "stderr": "Options '--number', '--papersize', '--orientation', '--rotation' are incompatible with positional arguments.\n",
    },
    {
        "command": ["-p", "0cmx0cm"],
        "returncode": 1,
        "stderr": "Error: I cannot produce pages with dimension 0x0.\n",
    },
]


class TestCommandLine(unittest.TestCase):
    """Run binary, and check produced files."""

    def assertPdfEqual(self, filea, fileb):
        """Test whether PDF files given in argument (as file names) are equal.

        Equal means: they look the same.
        """
        # pylint: disable=invalid-name
        images = (Image(filename=filea), Image(filename=fileb))

        # Check that files have the same number of pages
        self.assertEqual(len(images[0].sequence), len(images[1].sequence))

        # Check if pages look the same
        for pagea, pageb in zip(images[0].sequence, images[1].sequence):
            self.assertEqual(pagea.compare(pageb, metric="absolute")[1], 0)

    def test_commandline(self):
        """Test binary, from command line to produced files."""
        for data in FIXTURES:
            with self.subTest(**data):
                for filename in data.get("remove", ()):
                    try:
                        os.remove(filename)
                    except FileNotFoundError:
                        pass
                completed = subprocess.run(
                    EXECUTABLE + ["-m", "dummypdf"] + data["command"],
                    capture_output=True,
                    text=True,
                    check=False,
                )

                for key in ["returncode", "stderr", "stdout"]:
                    if key in data:
                        self.assertEqual(getattr(completed, key), data.get(key))

                if "diff" in data:
                    self.assertPdfEqual(*data["diff"])
