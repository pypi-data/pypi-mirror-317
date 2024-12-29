==========================================================================
bisos.graphviz: Python graphviz wrapped into BISOS CS and Seed Machinaries
==========================================================================

:Author: Mohsen BANAN
:Date:   <2024-02-19 Mon 16:27>

.. contents::
   :depth: 3
..

| ``Blee Panel Controls``: `Show-All <elisp:(show-all)>`__ \|
  `Overview <elisp:(org-shifttab)>`__ \|
  `Content <elisp:(progn (org-shifttab) (org-content))>`__ \|
  `(1) <elisp:(delete-other-windows)>`__ \|
  `S&Q <elisp:(progn (save-buffer) (kill-buffer))>`__ \|
  `Save <elisp:(save-buffer)>`__ \| `Quit <elisp:(kill-buffer)>`__ \|
  `Bury <elisp:(bury-buffer)>`__
| ``Panel Links``: `Blee Panel <../_nodeBase_/fullUsagePanel-en.org>`__
  \| `Github
  Panel <./py3/panels/bisos.facter/_nodeBase_/fullUsagePanel-en.org>`__
  ``See Also``: `At PYPI <https://pypi.org/project/bisos.facter>`__ \|
  `bisos.PyCS <https://github.com/bisos-pip/pycs>`__ \|
  `bisos.cmdb <https://github.com/bisos-pip/cmdb>`__

Overview
========

bisos.graphviz ()

bisos.graphviz is a python package that uses the PyCS-Framework for
processing graphviz specifications in python. It is a BISOS-Capability
and a Standalone-BISOS-Package.

*bisos.graphviz* is based on PyCS-Foundation and can be used both as a
Command and as a Service (invoke/perform model of remote operations)
using RPYC for central management of multiple systems.

.. _table-of-contents:

Table of Contents TOC
=====================

-  `Overview <#overview>`__
-  `Part of BISOS — ByStar Internet Services Operating
   System <#part-of-bisos-----bystar-internet-services-operating-system>`__
-  `bisos.graphviz is a Command Services (PyCS)
   Facility <#bisosgraphviz-is-a-command-services-pycs-facility>`__
-  `Uses of bisos.graphviz <#uses-of-bisosgraphviz>`__
-  `bisos.graphviz as a Standalone Piece of
   BISOS <#bisosgraphviz-as-a-standalone-piece-of-bisos>`__
-  `Installation <#installation>`__

   -  `Installation With pip <#installation-with-pip>`__
   -  `Installation With pipx <#installation-with-pipx>`__

-  `Usage <#usage>`__

   -  `Locally (system command-line) <#locally-system-command-line>`__
   -  `Remotely (as a service –
      Performer+Invoker) <#remotely-as-a-service----performerinvoker>`__

      -  `Performer <#performer>`__
      -  `Invoker <#invoker>`__

   -  `Use by Python script <#use-by-python-script>`__

      -  `bisos.graphviz Source Code is in writen in COMEEGA
         (Collaborative Org-Mode Enhanced Emacs Generalized Authorship)
         – <#bisosgraphviz-source-code-is-in-writen-in-comeega-collaborative-org-mode-enhanced-emacs-generalized-authorship----httpsgithubcombx-bleecomeega>`__\ https://github.com/bx-blee/comeega\ `. <#bisosgraphviz-source-code-is-in-writen-in-comeega-collaborative-org-mode-enhanced-emacs-generalized-authorship----httpsgithubcombx-bleecomeega>`__
      -  `The primary API for bisos.graphviz is
         ./bisos/graphviz/graphviz-csu.py. It is self documented in
         COMEEGA. <#the-primary-api-for-bisosgraphviz-is-bisosgraphvizgraphviz-csupy-it-is-self-documented-in-comeega>`__

-  `Documentation and Blee-Panels <#documentation-and-blee-panels>`__

   -  `bisos.graphviz Blee-Panels <#bisosgraphviz-blee-panels>`__

-  `Support <#support>`__

Part of BISOS — ByStar Internet Services Operating System
=========================================================

| Layered on top of Debian, **BISOS**: (By\* Internet Services Operating
  System) is a unified and universal framework for developing both
  internet services and software-service continuums that use internet
  services. See `Bootstrapping ByStar, BISOS and
  Blee <https://github.com/bxGenesis/start>`__ for information about
  getting started with BISOS.
| **BISOS** is a foundation for **The Libre-Halaal ByStar Digital
  Ecosystem** which is described as a cure for losses of autonomy and
  privacy in a book titled: `Nature of
  Polyexistentials <https://github.com/bxplpc/120033>`__

*bisos.graphviz* is part of BISOS.

bisos.graphviz is a Command Services (PyCS) Facility
====================================================

bisos.graphviz can be used locally on command-line or remotely as a
service. bisos.graphviz is a PyCS multi-unit command-service. PyCS is a
framework that converges developement of CLI and Services. PyCS is an
alternative to FastAPI, Typer and Click.

bisos.graphviz uses the PyCS Framework to:

#. Provide access to graphviz facilities through native python.
#. Provide local access to graphviz facilities on CLI.
#. Provide remote access to graphviz facilities through remote
   invocation of python Expection Complete Operations using
   `rpyc <https://github.com/tomerfiliba-org/rpyc>`__.
#. Provide remote access to graphviz facilities on CLI.

What is unique in the PyCS-Framework is that these four models are all a
single abstraction.

The core of PyCS-Framework is the *bisos.b* package (the
PyCS-Foundation). See https://github.com/bisos-pip/b for an overview.

Uses of bisos.graphviz
======================

Within BISOS, bisos.graphviz is used as a common facility.

bisos.graphviz as a Standalone Piece of BISOS
=============================================

bisos.graphviz is a standalone piece of BISOS. It can be used as a
self-contained Python package separate from BISOS. Follow the
installtion and usage instructions below for your own use.

Installation
============

The sources for the bisos.graphviz pip package is maintained at:
https://github.com/bisos-pip/graphviz.

The bisos.graphviz pip package is available at PYPI as
https://pypi.org/project/bisos.graphviz

You can install bisos.graphviz with pip or pipx.

Installation With pip
---------------------

If you need access to bisos.graphviz as a python module, you can install
it with pip:

.. code:: bash

   pip install bisos.graphviz

Installation With pipx
----------------------

If you only need access to bisos.graphviz as a command on command-line,
you can install it with pipx:

.. code:: bash

   pipx install bisos.graphviz

The following commands are made available:

-  graphviz.cs
-  roInv-graphviz.cs
-  roPerf-graphviz.cs

These are all one file with 3 names. *roInv-graphviz.cs* and
*roPerf-graphviz.cs* are sym-links to *graphviz.cs*

Usage
=====

Locally (system command-line)
-----------------------------

``graphviz.cs`` can be invoked directly as

.. code:: bash

   bin/graphviz.cs

Remotely (as a service – Performer+Invoker)
-------------------------------------------

You can also run

Performer
~~~~~~~~~

Run performer as:

.. code:: bash

   bin/roPerf-graphviz.cs

Invoker
~~~~~~~

Run invoker as:

.. code:: bash

   bin/roInv-graphviz.cs

Use by Python script
--------------------

bisos.graphviz Source Code is in writen in COMEEGA (Collaborative Org-Mode Enhanced Emacs Generalized Authorship) – https://github.com/bx-blee/comeega.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The primary API for bisos.graphviz is ./bisos/graphviz/graphviz-csu.py. It is self documented in COMEEGA.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Documentation and Blee-Panels
=============================

bisos.graphviz is part of ByStar Digital Ecosystem
http://www.by-star.net.

This module's primary documentation is in the form of Blee-Panels.
Additional information is also available in:
http://www.by-star.net/PLPC/180047

bisos.graphviz Blee-Panels
--------------------------

bisos.graphviz Blee-Panles are in ./panels directory. From within Blee
and BISOS these panles are accessible under the Blee "Panels" menu.

Support
=======

| For support, criticism, comments and questions; please contact the
  author/maintainer
| `Mohsen Banan <http://mohsen.1.banan.byname.net>`__ at:
  http://mohsen.1.banan.byname.net/contact
