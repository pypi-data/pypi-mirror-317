Welcome to `dummypdf`'s documentation!
======================================

This tool can produce dummy PDF files. They can be used to test software
manipulating such PDF files.

The produced files contain:

- a big page number;
- a rectangle around the page, and a cross across the whole page.

The color, page format and number of pages can be configured.

Examples:

- One page A4 paper: :download:`example1 <examples/example1.pdf>`

      dummypdf A4

- Six pages, a third of an A4 paper: :download:`example2 <examples/example2.pdf>`

      dummypdf -n 6 -p 21cmx99mm

  or:

      dummypdf 21cmx99mm:6

- A pdf with different page formats: :download:`different.pdf <examples/different.pdf>`

      dummypdf A4 A5:landscapewest

Download and install
--------------------

See the `project main page <http://framagit.org/spalax/dummypdf>`__, and
`changelog <https://framagit.org/spalax/dummypdf/blob/main/CHANGELOG.md>`_.

Usage
-----

Here are the command line options for `dummypdf`.

.. argparse::
    :module: dummypdf.__main__
    :func: commandline_parser
    :prog: dummypdf

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
