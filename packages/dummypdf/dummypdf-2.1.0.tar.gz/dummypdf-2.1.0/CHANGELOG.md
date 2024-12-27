* dummypdf 2.1.0 (2024-12-27)

    * Add Python3.13 support.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 2.0.0 (2023-09-24)

    * Drop python3.7 support; add python3.12 support.
    * Backward-incompatible changes
        * Output file is given with option -o; orientation is given with option -O.
        * Remove option --list: positional arguments are now used instead.
    * Options
        * New option: --rotation
        * Option --orientation is now incompatible with --list.
        * Orientation and rotation can be set in positional arguments.
    * Hidden internal refactoring.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 1.4.0 (2022-11-29)

    * Python3.11 support.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 1.3.0 (2021-11-27)

    * Add Python3.10 support.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 1.2.0 (2021-06-20)

    * Option `--orientation` is no longer ignored (closes #6).
    * Python support
      * Drop python3.5 and python3.6 support
      * Add python3.8 and python3.9 support

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 1.1.0 (2019-03-08)

    * Features and bugs
      * Can write output to standard output (closes #4).
    * Python support
      * Add python3.7 support (closes #5).
      * Drop python3.4 support.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 1.0.0 (2017-12-12)

    * No changes since previous version.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 0.3.0 (2017-03-12)

    * Null paper sizes (e.g. `--papersize=0cmx1cm`) are no longer ignored (closes #2).
    * New option `--list`: it is now possible to create files with several page sizes (closes #3).
    * Add python3.6 support.
    * Add regression tests.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 0.2.1 (2016-10-14)

    * Move help about available color names into a separate "--list-colors" option.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 0.2.0 (2016-05-21)

    * Can generate PDFs with no pages.
    * Can be called using `python -m dummypdf`.
    * Several minor improvements to setup.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 0.1.1 (2015-06-13)

    * Several minor improvements to setup, test and documentation.

    -- Louis Paternault <spalax@gresille.org>

* dummypdf 0.1.0 (2015-03-15)

    * First published version.

    -- Louis Paternault <spalax@gresille.org>
