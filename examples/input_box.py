import vscode

ext = vscode.Extension(name="firstext", display_name="First Ext", version="0.0.1")

@ext.command()
def input_box():
    options = vscode.ext.InputBoxOptions(title='Enter your name')
    response = vscode.window.show_input_box(options)

    if not response: 
        return # stops execution if response is undefined or empty
        
    vscode.window.show_info_message(f"Your name reversed is: {response[::-1]}")

vscode.build(ext)