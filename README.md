# vscode-ext

This package allows you to create vscode extensions with python.

## Installation

Stable version:

```
pip install vscode-ext
```

Working version: `pip install git+https://github.com/CodeWithSwastik/vscode-ext`

## Why use this?

Why should you use this for building VScode extensions when you can use typescript? Here are some reasons:

- vscode-ext builds the package.json for you! No need to switch between your extension.py and package.json in order to add commands. It also handles adding Activity Bars, Keybinds and Views.
- vscode-ext provides a more pythonic way of creating the extension. Python also has some powerful modules that Javascript doesn't and you can include these with vscode-ext
- vscode-ext extensions work perfectly with vsce and you can publish your extensions just like you would publish any other extension.

## Tutorial

### Step 1:

Create a python file inside a folder.

![image](https://user-images.githubusercontent.com/61446939/126891766-8e408f35-ce63-48b1-8739-1361e979d351.png)

### Step 2:

Write the code for your extension. For this tutorial we have used the [Example Extension](#example-extension)

![image](https://user-images.githubusercontent.com/61446939/126891803-8da2e8e8-174f-451b-9103-4fbf001c4e7b.png)

### Step 3:

Run the python file. It will build the files.

![image](https://user-images.githubusercontent.com/61446939/126891865-fe235598-9267-47c6-971f-43e4da456ebb.png)
![image](https://user-images.githubusercontent.com/61446939/126891875-62c2057e-e504-4e01-bfd6-9a20c7f660d9.png)

### Step 4:

Press F5. This will run the extension and open a new vscode window in development mode.

### Step 5:

Finally, test your command.

- Open the command palette with Ctrl+P

![image](https://user-images.githubusercontent.com/61446939/126892044-f3b5f4d3-37de-4db5-acef-c6ddd841f1a5.png)

- Type `>Hello World`

![image](https://user-images.githubusercontent.com/61446939/126892096-9fc1cb2f-9b76-4d53-8099-e74d9f22e6e7.png)

- It should show a popup like this in the bottem right corner

![image](https://user-images.githubusercontent.com/61446939/126892110-f8d4bcf2-9ec0-43c2-a7d6-40288d91f000.png)

## Example Extension

```python
import vscode

ext = vscode.Extension(name = "testpy", display_name = "Test Py", version = "0.0.1")

@ext.event
def on_activate():
    return f"The Extension '{ext.name}' has started"

@ext.command()
def hello_world():
    vscode.window.show_info_message(f'Hello World from {ext.name}')

@ext.command()
def ask_question():
    res = vscode.window.show_info_message('How are you?', 'Great', 'Meh')
    if res == "Great":
        vscode.window.show_info_message('Woah nice!!')
    elif res == "Meh":
        vscode.window.show_info_message('Sorry to hear that :(')
vscode.build(ext)
```
## Extensions built using vscode-ext
Here's a list of some extensions built using vscode-ext. If you'd like to include your extension here feel free to create a PR.
- [Youtube](https://github.com/CodeWithSwastik/youtube-ext) 


## Documentation

Coming soon!
