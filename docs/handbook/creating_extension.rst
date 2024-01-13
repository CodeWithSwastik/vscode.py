Creating your first extension
=============================

Getting Started
----------------

Create a folder and place a Python file inside it.

.. image:: https://user-images.githubusercontent.com/61446939/126891766-8e408f35-ce63-48b1-8739-1361e979d351.png


Write Extension Code
---------------------

.. code-block:: python

    import vscode
    from vscode import InfoMessage

    ext = vscode.Extension(name="Test Extension")

    @ext.event
    async def on_activate():
        vscode.log(f"The Extension '{ext.name}' has started")

    @ext.command()
    async def hello_world(ctx):
        return await ctx.show(InfoMessage(f"Hello World from {ext.name}"))

    ext.run()

Run the Python File
--------------------

Execute the Python file. This action will build the necessary files.

.. image:: https://user-images.githubusercontent.com/61446939/126891865-fe235598-9267-47c6-971f-43e4da456ebb.png
.. image:: https://user-images.githubusercontent.com/61446939/126891875-62c2057e-e504-4e01-bfd6-9a20c7f660d9.png

Run the Extension
------------------

Press F5. This will initiate the extension and open a new VSCode window in development mode.

Test Your Command
------------------

- Open the command palette in the development window with `Ctrl+P`.
  
  .. image:: https://user-images.githubusercontent.com/61446939/126892044-f3b5f4d3-37de-4db5-acef-c6ddd841f1a5.png

- Type ``>Hello World`` in the command palette.
  
  .. image:: https://user-images.githubusercontent.com/61446939/126892096-9fc1cb2f-9b76-4d53-8099-e74d9f22e6e7.png

- The popup message should appear in the bottom right corner.
  
  .. image:: https://user-images.githubusercontent.com/61446939/126892110-f8d4bcf2-9ec0-43c2-a7d6-40288d91f000.png