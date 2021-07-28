import vscode

ext = vscode.Extension(name="example", display_name="Example Ext", version="0.0.1")

@ext.command()
def quick_pick():

    # items can be a list of strings, dicts or QuickPickItem
    items = [
        vscode.ext.QuickPickItem(
            label='Youtube', 
            detail='A video sharing platform'   
        ), 
        vscode.ext.QuickPickItem(
            label='Github', 
            detail='A code sharing platform'   
        ), 
    ]

    options = vscode.ext.QuickPickOptions(match_on_detail=True)
    selected = vscode.window.show_quick_pick(items, options)
    
    if not selected: 
        return # stops execution if selected is undefined or empty
        
    # selected will either be a string or QuickPickItem 
    # depending on the items you supplied
    # TIP: For consistency use either strings or QuickPickItems 
    # don't use both together 

    vscode.window.show_info_message(f"Your selected {selected.label}")

vscode.build(ext)