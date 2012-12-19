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

    -- Comments start with double dash and go until end of line.
    -- Project id and title:
    project 2233 "Development of a PPL compiler"

    -- A task with subtasks:
    task DOC "Documentation"
        INFR "Infrastructure and scripts for rst -> html compilation"
        -- Implicitly assumes 'task' as the command because we're inside
        -- another task. Also because of indent the task created by this
        -- line will be a subtask of DOC. So the line is equivalent to:
        -- task DOC.INFR ....
        PPL  "PPL general description"
        COMP "Compiler user manual" (requires DEV.COMP) -- embedded dependency

    tasks:
    -- Lines without explicit type will be treated as tasks until the mode
    -- is switched by a similar command
    DEV "Development"
        SETUP "Setting up the product"
            VCS "Version control" (estimate: 1h)
            MK  "Makefile" (estimate: 30m) -- estimate
            VE  "Virtual environment setup (Just add the section to the
                 makefile)" (estimate: 10m)
            -- Text inside quotes can span multiple lines. This is treated as
            -- if it was all on one line and the lines are joined stripping
            -- extra spaces.
            TST "Unit testing" (estimate: 30m, requires MK) 
            -- Estimate and dependency. Not fully qualified names can be used
            -- as long as they can be unambiguously resolved. Colons after
            -- 'estimate' and 'requires' are optional. Canonically there is a
            -- colon after 'estimate' and no colon after 'requires' because
            -- this is easier to read.

        LIB   "Library" 
            DATA "Data model" (required by PARS) -- dependency from other side
            PARS "Parser"
            PROC "Processors"
                LVL "Levelling"

        COMP  "Compiler" (estimate: 4d)
        PDF   "PDF generator" (estimate: 4d 4h)

    estimates:
    -- Now default becomes estimates
    DOC
        INFR: 30m
        PPL: 8h
        COMP: 4h 30m
    DEV
        DATA, PARS, PROC: 2d -- estimating multiple tasks at once

    dependencies:
    -- And now dependencies
    DOC <- SETUP.MK
        INFR -> PPL, COMP -- multiple dependants
    DEV
        SETUP -> LIB, COMP, PDF
            VCS -> MK -> TST -- such syntax might be useful for long chains
        COMP, PDF <- LIB
        LIB
            PROC requires DATA, PARS -- 'requires' is an alias for '<-'

    dependency INFR <- VE
    -- Not qualified ids are ok as long as there's no ambiguity. If ambiguity
    -- is possible but can be resolved, a warning can be generated. Ambiguity
    -- can be eliminated by adding more parents or by prefixing the id with
    -- a dot if the id is top level.

