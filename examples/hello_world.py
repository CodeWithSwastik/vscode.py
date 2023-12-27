import vscode

ext = vscode.Extension(name="Test Extension")


@ext.event
async def on_activate():
    vscode.log(f"The Extension '{ext.name}' has started")


@ext.command()
async def hello_world(ctx):
    return await ctx.show(vscode.InfoMessage(f"Hello World from {ext.display_name}"))


ext.run()
