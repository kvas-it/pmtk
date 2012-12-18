Project Plan Language
=====================

:Author: Vasily Kuznetsov

Background
----------

Project plan language (PPL) is a DSL for describing project plans. It provides
a simple and programmer-friendly way to describe the plan of a project that can
be later processed with various tools to produce the desired artifacts.

Language structure
------------------

PPL code consists of statements that describe various aspects of a project
(work breakdown, effort estimates, constraints, resources, calendar, etc.). The
intention is to make PPL source files as easily readable and as compact as
possible. For many things there is more than one way to do it, but there's
always a canonical way to do things which is used by the toolchain when writing
PPL.

Indentation is used for denoting blocks. Block starts from increased
indentation and goes until the indentation goes back to one of higher levels.
Decreasing indentation in such a way that it doesn't correspond to any of the
higher levels is a syntax error. Both spaces and tabs can be used for
indentation with tab being equal to eight spaces. The canonical way is to use
only spaces and to increase indentation by four spaces for each level.

Example
-------

Typical project plan expressed in PPL::

    project 2233 "Development of a PPL compiler"

    task DOC "Documentation"
        INFR "Infrastructure and scripts for rst -> html compilation"
        PPL  "PPL general description"
        COMP "Compiler user manual" (requires DEV.COMP)

    task DEV "Development"
        SETUP "Setting up the product"
            VCS "Version control" (estimate = 1h)
            MK  "Makefile" (estimate = 30m)
            TST "Unit testing" (estimate = 30m, requires MK)

        LIB   "Library" 
            DATA "Data model" (required by PARS)
            PARS "Parser"
            PROC "Processors"
                LVL "Levelling"

        COMP  "Compiler" (estimate = 4d)
        PDF   "PDF generator" (estimate = 4d)

    estimates
        DOC
            INFR = 30m
            PPL = 8h
            COMP = 4h
        DEV
            DATA, PARS, PROC = 2d

    dependencies
        DEV
            COMP, PDF <- LIB
            LIB
                PROC <- DATA, PARS

