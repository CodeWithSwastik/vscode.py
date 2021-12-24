import vscode

ext = vscode.Extension(name="Example Ext")


@ext.command()
async def input_box(ctx):
    box = vscode.InputBox(title="Enter your name")
    response = await ctx.show(box)

    if not response:
        return  # stops execution if response is undefined or empty

    await ctx.show(vscode.InfoMessage(f"Your name reversed is: {response[::-1]}"))


ext.run()
