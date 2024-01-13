Publishing Extensions
=====================

To publish your extension created with ``vscode.py``, execute your extension file with the ``--publish`` flag:

.. code-block:: bash

    python extension.py --publish

This command will generate the ``README.md`` and ``CHANGELOG.md`` for your extension. Keeping these files updated is important. Additionally, it will create the `.vscodeignore` file. The contents specified in this file will be excluded from packaging in your extension.

Afterward, follow the steps outlined in the `official documentation for publishing extensions`_.


.. _official documentation for publishing extensions: https://code.visualstudio.com/api/working-with-extensions/publishing-extension