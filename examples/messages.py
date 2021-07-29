import vscode

ext = vscode.Extension(name="messages", display_name="Messages", version="0.0.1")


@ext.command()
def info():
    vscode.window.show_info_message("This is an info message")


@ext.command()
def warn():
    vscode.window.show_warn_message("This is a warning message")


@ext.command()
def error():
    vscode.window.show_error_message("This is an error message")


@ext.command()
def show_choices():
    # This works the same with warning and error
    choice = vscode.window.show_info_message("Are you happy using this?", "Yes", "No")

    if not choice:
        return
    elif choice == "Yes":
        vscode.window.show_info_message("Thanks :)")
    else:
        vscode.window.show_info_message(":(")


vscode.build(ext)
