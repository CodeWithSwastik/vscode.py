import vscode

ext = vscode.Extension(name="firstext", display_name="First Ext", version="0.0.1")

@ext.event
def on_activate():
    return f"The Extension '{ext.name}' has started"

@ext.command()
def hello_world():
    vscode.window.show_info_message(f"Hello World from {ext.display_name}")

vscode.build(ext)
