import vscode

ext = vscode.Extension(name="Test Extension")


@ext.event
async def on_activate():
    vscode.log(f"The Extension '{ext.name}' has started")


@ext.command(keybind="f8")
async def hello_world(ctx):
    return await ctx.show(vscode.InfoMessage(f"Hello World from {ext.name}"))


@ext.command(keybind="f9", when="editor_lang_id == python")
async def ask_question(ctx):

    resp = await ctx.show(vscode.InfoMessage("How are you?", ("Great!", "Sad")))
    if resp == "Great!":
        await ctx.show(vscode.InfoMessage("Thats nice!"))
    elif resp == "Sad":
        box = vscode.InputBox(prompt="Sorry to hear that, could you tell us why?")
        res = await ctx.show(box)
        await ctx.show(vscode.InfoMessage(res))


@ext.command()
async def show_picker(ctx):
    items = [
        vscode.QuickPickItem("apple", detail="A fruit"),
        vscode.QuickPickItem("boring", detail="An adjective"),
        vscode.QuickPickItem("cat", detail="An animal"),
    ]
    res = ctx.show(
        vscode.QuickPick(items, vscode.QuickPickOptions(match_on_detail=True))
    )

    if not res:
        return

    await ctx.show(vscode.InfoMessage(f"Woah you selected: '{res.label}'"))


ext.run()