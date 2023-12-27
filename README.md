<p align="center">
  <img alt="vscode.py logo" src="https://github.com/CodeWithSwastik/vscode.py/blob/main/images/vscode-py.png?raw=true" width='500px'/>
</p>

<p align="center"><a href="https://GitHub.com/CodeWithSwastik/vscode.py/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" alt="Maintenance"></a>
<a href="https://pepy.tech/project/vscode.py"><img src="https://static.pepy.tech/personalized-badge/vscode.py?period=total&amp;units=international_system&amp;left_color=orange&amp;right_color=brightgreen&amp;left_text=Downloads" alt="Downloads"></a>
<a href="https://pypi.python.org/pypi/vscode.py/"><img src="https://badge.fury.io/py/vscode.py.svg" alt="PyPI version"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## About

Create vscode extensions with python.

## Installation

Stable version:

```sh-session
pip install vscode.py
```

## Why use vscode.py?

Why should you use this for building VScode extensions when you can use typescript? Here are some reasons:

- vscode.py builds the package.json for you! No need to switch between your extension.py and package.json in order to add commands. It also handles adding Activity Bars, Keybinds and Views.
- vscode.py provides a pythonic way of creating the extension. Python has some powerful modules that Javascript doesn't and you can include these with vscode.py
- vscode.py extensions work perfectly with vsce and you can publish your extensions just like you would publish any other extension.

## Example Extension

```python
import vscode
from vscode import InfoMessage

ext = vscode.Extension(name="Test Extension")

@ext.event
async def on_activate():
    vscode.log(f"The Extension '{ext.name}' has started")


@ext.command()
async def hello_world(ctx):
    return await ctx.show(InfoMessage(f"Hello World from {ext.name}"))

ext.run()
```

## Tutorial

### Step 1

Create a python file inside a folder.

![image](https://user-images.githubusercontent.com/61446939/126891766-8e408f35-ce63-48b1-8739-1361e979d351.png)

### Step 2

Write the code for your extension. For this tutorial we have used the [Example Extension](#example-extension)

### Step 3

Run the python file. It will build the required extension files.

![image](https://user-images.githubusercontent.com/61446939/126891865-fe235598-9267-47c6-971f-43e4da456ebb.png)
![image](https://user-images.githubusercontent.com/61446939/126891875-62c2057e-e504-4e01-bfd6-9a20c7f660d9.png)

### Step 4

Press F5. This will run the extension and open a new vscode window in development mode.

### Step 5

Finally, test your command.

- Open the command palette with Ctrl+P in the development window.

![image](https://user-images.githubusercontent.com/61446939/126892044-f3b5f4d3-37de-4db5-acef-c6ddd841f1a5.png)

- Type `>Hello World`

![image](https://user-images.githubusercontent.com/61446939/126892096-9fc1cb2f-9b76-4d53-8099-e74d9f22e6e7.png)

- It should show a popup like this in the bottom right corner

![image](https://user-images.githubusercontent.com/61446939/126892110-f8d4bcf2-9ec0-43c2-a7d6-40288d91f000.png)

## Extensions built using vscode.py

Here's a list of some extensions built using vscode.py. If you'd like to include your extension here feel free to create a PR.

- [Youtube](https://github.com/CodeWithSwastik/youtube-ext)
- [Wikipedia](https://github.com/SkullCrusher0003/wikipedia-ext)
- [Internet Search](https://github.com/Dorukyum/internet-search)
- [Virtual Assistant](https://github.com/SohamGhugare/vscode-virtual-assistant)
- [YoExtension](https://github.com/yo56789/YoExtension)

## Documentation

The docs are coming soon! In the meantime you can look at the [examples](https://github.com/CodeWithSwastik/vscode.py/tree/main/examples) in order to learn how vscode.py works and what it offers!
