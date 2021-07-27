import vscode

ext = vscode.Extension(name="test py", display_name="Test Py", version="0.0.2")
ext.set_activity_bar(
    vscode.ext.ActivityBar(id=ext.name, title=ext.display_name, icon="media/python.svg"),
    vscode.ext.StaticWebview(f"{ext.name}.activity", html ='<h1>Welcome"!</h1>')
)


@ext.event
def on_activate():
    return f"The Extension '{ext.name}' has started"


@ext.command(keybind="f8")
def hello_world():
    return vscode.window.show_info_message(f"Hello World from {ext.name}")


@ext.command(keybind="f9", when="editor_lang_id == python")
def ask_question():
    res = vscode.window.show_info_message("How are you?", "Great", "Meh")
    if res == "Great":
        vscode.window.show_info_message("Woah nice!!")
    elif res == "Meh":
        options = vscode.ext.InputBoxOptions(prompt='Sorry to hear that, could you tell us why?')
        res = vscode.window.show_input_box(options)
        vscode.window.show_info_message(res)
        

@ext.command()
def show_picker():
    data = [
        {"label": "apple", "detail": "A fruit"},
        {"label": "boring", "detail": "An adjective"},
    ]
    res = vscode.window.show_quick_pick(data, vscode.ext.QuickPickOptions(match_on_detail=True))
    if res == vscode.undefined:
        return print(type(res))
    vscode.window.show_info_message(f"Nice you chose {res['label']}")


vscode.build(ext)
