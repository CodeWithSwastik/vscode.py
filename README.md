# vscode

This package allows you to create vscode extensions with python. It does so by transpiling the python code to javascript.

## Installation

Stable version:

```
pip install vscode-ext
```

Working version:

```
pip install git+https://github.com/CodeWithSwastik/vscode
```

## Tutorial

Comming soon!

## Example Extension

```python
import vscode

ext = vscode.Extension(name="testpy", display_name="Test Py", version = "0.0.1")

@ext.event
def on_activate():
    return f"The Extension '{ext.name}' has started"

@ext.command()
def hello_world():
    return vscode.window.show_info_message(f'Hello World from {ext.name}')

vscode.build(ext)
```
