## Example

#### Code

```py
import vscode
from vscode import Config, InfoMessage

c = Config(name='Say', description='Say Something!', input_type=str, default="Hello World!")
ext = vscode.Extension(name='Speaker', config=[c])

@ext.command()
async def message_say_config(ctx):
    say_value = await ctx.workspace.get_config_value(c)
    await ctx.window.show(InfoMessage(say_value))

ext.run()
```

#### Result

<img src="https://i.imgur.com/LkCwdCT.gif"/>

# Workspace Configurations

::: vscode.config
