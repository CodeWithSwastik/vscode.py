## Example

#### Code

```py
import vscode
from vscode.config import Config

c = Config(name='Say', description='Say Something!', input_type=str, default="Hello World!")
ext = vscode.Extension('speaker','Speaker', '0.0.1', config=[c])

@ext.command()
def message_say_config():
    vscode.window.show_info_message(ext.get_config('Say') or c.default)

vscode.build(ext)
```

#### Result

<img src="https://i.imgur.com/LkCwdCT.gif"/>

# Workspace Configurations

::: vscode.config
