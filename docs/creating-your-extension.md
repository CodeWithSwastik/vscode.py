## Guide

### Step 1

Create a python file inside a folder.

![image](https://user-images.githubusercontent.com/61446939/126891766-8e408f35-ce63-48b1-8739-1361e979d351.png)

### Step 2

Write the code for your extension. For this guide we have used the [Example Extension](#example-extension)

![image](https://user-images.githubusercontent.com/61446939/126891803-8da2e8e8-174f-451b-9103-4fbf001c4e7b.png)

### Step 3

Run the python file. It will build the files.

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
