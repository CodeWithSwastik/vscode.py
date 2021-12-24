import vscode

ext = vscode.Extension(name="Example Ext")

@ext.command()
async def quick_pick(ctx):

    # items can be a list of strings, dicts or QuickPickItem
    items = [
        vscode.QuickPickItem(label="Youtube", detail="A video sharing platform"),
        vscode.QuickPickItem(label="Github", detail="A code sharing platform"),
    ]

    options = vscode.QuickPickOptions(match_on_detail=True)
    selected = await ctx.window.show(vscode.QuickPick(items, options))

    if not selected:
        return  # stops execution if selected is undefined or empty

    # selected will either be QuickPickItem
    # or a list of QuickPickItem
    # if can_pick_many was set to True 

    await ctx.window.show(vscode.InfoMessage(f"You selected: {selected.label}"))

ext.run()
