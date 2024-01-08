.. vscode.py documentation master file, created by
   sphinx-quickstart on Wed Dec 27 13:07:00 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

vscode.py
=========

.. image:: https://img.shields.io/badge/Maintained%3F-yes-green.svg
   :alt: Maintenance
   :target: https://GitHub.com/CodeWithSwastik/vscode.py/graphs/commit-activity

.. image:: https://static.pepy.tech/personalized-badge/vscode.py?period=total&units=international_system&left_color=orange&right_color=brightgreen&left_text=Downloads
   :alt: Downloads
   :target: https://pepy.tech/project/vscode.py

.. image:: https://badge.fury.io/py/vscode.py.svg
   :alt: PyPi Version
   :target: https://pypi.python.org/pypi/vscode.py/

.. image:: https://img.shields.io/github/stars/CodeWithSwastik/vscode.py.svg?style=social&label=Star&maxAge=2592000
   :alt: Github Stars
   :target: https://GitHub.com/CodeWithSwastik/vscode.py/stargazers/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :alt: Code Style: Black
   :target: https://github.com/psf/black

Create vscode extensions with python.

Why use vscode.py?
------------------
Why should you use this for building VScode extensions when you can use typescript? Here are some reasons:

- **vscode.py** builds the package.json for you! No need to switch between your extension.py and package.json in order to add commands. It also handles adding **Activity Bars**, **Keybinds** and **Views**.

- **vscode.py** provides a more **pythonic way** of creating the extension. Python also has some powerful modules that Javascript doesn't and you can include these with vscode.py

- **vscode.py** extensions work perfectly with vsce and you can publish your extensions just like you would publish any other extension.

Extensions built using vscode.py
--------------------------------
Here's a list of some extensions built using vscode.py. If you'd like to include your extension here feel free to create a PR.

- `YouTube <https://github.com/CodeWithSwastik/youtube-ext>`_

- `Wikipedia <https://github.com/SkullCrusher0003/wikipedia-ext>`_

- `Internet Search <https://github.com/Dorukyum/internet-search>`_

- `Virtual Assistant <https://github.com/SohamGhugare/vscode-virtual-assistant>`_


.. toctree::
   :maxdepth: 1
   :caption: Tables of Content

   handbook/index
   reference/index
   misc/index

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`