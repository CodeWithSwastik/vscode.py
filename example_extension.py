import vscode

ext = vscode.Extension(name="testpy", display_name="Test Py", version = "0.0.1")

@ext.event
def on_activate():
    return f"The Extension '{ext.name}' has started"

@ext.command()
def hello_world():
    return vscode.window.show_info_message(f'Hello World from {ext.name}')

@ext.command(title='Cause Some Error')
def show_error():
    return vscode.window.show_error_message(f'Error!')

vscode.build(ext)