import vscode

ext = vscode.Extension(name="commands", display_name="Commands", version="0.0.1")

@ext.command()
def simple_command():
    # If a command title is not specified, vscode-ext removes the underscores
    # and title cases each word to be the title for the command
    # Eg: This command will become > Simple Command

    vscode.window.show_info_message(f"This is a command")

@ext.command(title = "Great Command")
def change_my_title():
    vscode.window.show_info_message(f"This is a Great command")

@ext.command(keybind = "F9")
def keybind_command():
    # You can add keybinds to your commands in this way
    vscode.window.show_info_message(f"This is will execute if you press F9")


@ext.command(keybind = "F10", when = "editor_lang_id == python")
def only_python():
    # You can add special conditions to your keybinds in this way
    # NOTE: The when condition only applies to the keybinds, the command can 
    # be triggered normally through the command palette

    vscode.window.show_info_message(f"This command")

vscode.build(ext)