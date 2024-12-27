dummypdf 🥼 Generate dummy pdf files
====================================

*Check out my other PDF tools:* `pdfautonup <https://framagit.org/spalax/pdfautonup>`__ | `pdfimpose <https://framagit.org/spalax/pdfimpose>`__.

Paper size and number of pages are configurable. Files can be used to test pdf
manipulation tools.

Examples :

- One page A4 paper: `example1.pdf <https://framagit.org/spalax/dummypdf/-/raw/main/doc/examples/example1.pdf?inline=false>`__:

      dummypdf A4

- Six pages, a third of an A4 paper: `example2.pdf <https://framagit.org/spalax/dummypdf/-/raw/main/doc/examples/example2.pdf?inline=false>`__:

      dummypdf -n 6 -p 21cmx99mm

  or:

      dummypdf 21cmx99mm:6

- A pdf with different page formats: `different.pdf <https://framagit.org/spalax/dummypdf/-/raw/main/doc/examples/different.pdf?inline=false>`__:

      dummypdf A4 A5:landscapewest

But why?
--------

To develop or test PDF manipulating tools, I sometimes need to have files with a very specific size or number of pages. I can generate those files with this tool.

What's new?
-----------

See `changelog <https://framagit.org/spalax/dummypdf/blob/main/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/dummypdf
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install dummypdf

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/dummypdf-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://dummypdf.readthedocs.io>`_

* To compile it from source, download and run::

    cd doc && make html
