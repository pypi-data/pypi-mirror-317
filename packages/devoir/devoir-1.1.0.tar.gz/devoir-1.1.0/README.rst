Devoir ✏️ Quickly set up a working environment to edit a file
=============================================================

When editing a LaTeX file, I want the file being edited with `vim <http://www.vim.org>`_, the compiled file displayed using a pdf viewer, and latex being run whenever something changes, using `latexmk <http://users.phys.psu.edu/~collins/software/latexmk-jcc/>`_. But wait, there is more.

- I often start a LaTeX document by copying an existing one, as a template.
- The pdf file may or may not exist when I start working: if I have already
  been working on this file before, the pdf file exists; if not, it does not
  exists, and my pdf viewer won't start on a non-existing file.

This program aims to automate all this process. I built it to process LaTeX
files, but it should work with other files too.

What's new?
-----------

See `changelog <https://git.framasoft.org/spalax/devoir/blob/main/CHANGELOG.md>`_.

Download and install
--------------------

See the end of list for a (quick and dirty) Debian package.

* From sources:

  * Download: https://pypi.python.org/pypi/devoir
  * Install (in a `virtualenv`, if you do not want to mess with your distribution installation system)::

        python3 setup.py install

* From pip::

    pip install devoir

* Quick and dirty Debian (and Ubuntu?) package

  This requires `stdeb <https://github.com/astraw/stdeb>`_ to be installed::

      python3 setup.py --command-packages=stdeb.command bdist_deb
      sudo dpkg -i deb_dist/devoir-<VERSION>_all.deb

Documentation
-------------

* The compiled documentation is available on `readthedocs <http://devoir.readthedocs.io>`_

* To compile it from source, download and run::

      cd doc && make html
