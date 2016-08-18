.. highlight:: shell

Getting Started
===============

Prerequisites
-----------------

* Git
* Python 2.7


Get the code
--------------------
Given you have privileges to access the codebase on GitHub, execute the following command on
a shell prompt::

  $ git clone git@github.com:BriefyHQ/briefy.plone.git

Local Install
--------------
Access the directory containing *briefy.plone* codebase::

  $ cd briefy.plone

Create a virtual environment::

  $ virtualenv .

Install package & dependencies
+++++++++++++++++++++++++++++++++++

Installing dependencies::


    $ ./bin/pip install -r requirements.txt


Running buildout::

    $ ./bin/buildout -c buildout.cfg


Running tests
-----------------------

Run all tests::

    $ make test


Reporting Bugs
--------------------------

Report bugs at https://github.com/BriefyHQ/briefy.plone/issues.

If you are reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
