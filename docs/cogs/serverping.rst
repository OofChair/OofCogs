.. _serverping:

==========
ServerPing
==========

This is the cog guide for the serverping cog. You will
find detailed docs about usage and commands.

``[p]`` is considered as your prefix.

.. note:: To use this cog, load it by typing this::

        [p]load serverping

.. _serverping-usage:

-----
Usage
-----

Ping a server.


.. _serverping-commands:

--------
Commands
--------

.. _serverping-command-pingversion:

^^^^^^^^^^^
pingversion
^^^^^^^^^^^

**Syntax**

.. code-block:: none

    [p]pingversion

**Description**

Check what version the cog is on.

.. _serverping-command-serverping:

^^^^^^^^^^
serverping
^^^^^^^^^^

**Syntax**

.. code-block:: none

    [p]serverping <server>

**Description**

Ping a server or an IP.

**Pinging a specific port will not work. This is due to restrictions with the lib.**

Example request: ``[p]serverping oofchair.xyz`` Adding https://, adding a trailing slash, or adding something after the / will cause this to not work.
