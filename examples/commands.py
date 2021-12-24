import vscode

ext = vscode.Extension(name="Commands Example")


@ext.command()
async def simple_command(ctx):
    # If a command title is not specified, vscode-ext removes the underscores
    # and title cases each word to be the title for the command
    # Eg: This command will become > Simple Command

    await ctx.window.show(vscode.InfoMessage("This is a command"))


@ext.command(title="Great Command")
async def change_my_title(ctx):
    await ctx.window.show(vscode.InfoMessage("This is a great command"))


@ext.command(keybind="F9")
async def keybind_command(ctx):
    # You can add keybinds to your commands in this way
    await ctx.window.show(vscode.InfoMessage("This is will execute if you press F9"))


@ext.command(keybind="F10", when="editor_lang_id == python")
async def only_python(ctx):
    # You can add special conditions to your keybinds in this way
    # NOTE: The when condition only applies to the keybinds, the command can
    # be triggered normally through the command palette

    await ctx.window.show(vscode.InfoMessage("Hi python user!"))


ext.run()
