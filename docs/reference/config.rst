Configurations
==============

.. code-block:: python
   
   import vscode
   from vscode import Config, InfoMessage

   c = Config(name='Say', description='Say Something!', input_type=str, default="Hello World!")
   ext = vscode.Extension(name='Speaker', config=[c])

   @ext.command()
   async def message_say_config(ctx):
      say_value = await ctx.workspace.get_config_value(c)
      await ctx.window.show(InfoMessage(say_value))

   ext.run()

.. image:: https://camo.githubusercontent.com/587f55ac991ccc42bec7f3432fbd86a68fa5e28ff9dc550f2350e7689f27710c/68747470733a2f2f692e696d6775722e636f6d2f4c6b43776443542e676966

.. automodule:: vscode.config
   :members:
   :undoc-members:
   :show-inheritance: