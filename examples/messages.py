import vscode

ext = vscode.Extension(name="Messages")


@ext.command()
async def info(ctx):
    await ctx.show(vscode.InfoMessage("This is an info message"))


@ext.command()
async def warn(ctx):
    await ctx.show(vscode.WarningMessage("This is a warning message"))


@ext.command()
async def error(ctx):
    await ctx.show(vscode.ErrorMessage("This is an error message"))


@ext.command()
async def show_choices(ctx):
    # This works the same with warning and error
    message = vscode.InfoMessage("Are you happy using this?", ["Yes", "No"])
    choice = await ctx.show(message)

    if not choice:
        return
    elif choice == "Yes":
        await ctx.show(vscode.InfoMessage("Thanks :)"))
    else:
        await ctx.show(vscode.InfoMessage(":("))


ext.run()
