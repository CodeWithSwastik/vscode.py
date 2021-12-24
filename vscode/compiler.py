import os
import time
import json
import venv
import inspect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vscode.extension import Extension

__all__ = ("build",)


def create_package_json(extension) -> None:
    package = {
        "name": extension.name,
        "displayName": extension.display_name,
        "main": "./extension.js",
        "contributes": {
            "commands": [cmd.to_dict() for cmd in extension.commands],
        },
        "activationEvents": [
            "onCommand:" + cmd.extension_string for cmd in extension.commands
        ],
    }
    first_info = {
        "version": "0.0.1",
        "engines": {"vscode": "^1.58.0"},
        "categories": ["Other"],
    }

    if extension.keybindings:
        package["contributes"].update({"keybindings": extension.keybindings})

    # package.update(config)

    cwd = os.getcwd()

    package_dir = os.path.join(cwd, "package.json")
    if os.path.isfile(package_dir):
        with open(package_dir, "r") as f:
            try:
                new_package = json.load(f)
                new_package.update(package)
            except json.decoder.JSONDecodeError:
                new_package = package.update(first_info)
    else:
        new_package = package.update(first_info)
    with open(package_dir, "w") as f:
        json.dump(new_package, f, indent=2)


def create_launch_json():
    launch_json = {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Run Extension",
                "type": "extensionHost",
                "request": "launch",
                "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
            },
        ],
    }

    cwd = os.getcwd()

    vscode_path = os.path.join(cwd, ".vscode")
    os.makedirs(vscode_path, exist_ok=True)
    os.chdir(vscode_path)

    with open("launch.json", "w") as f:
        json.dump(launch_json, f, indent=2)

    os.chdir(cwd)


REGISTER_COMMANDS_TEMPLATE = """
  context.subscriptions.push(
    vscode.commands.registerCommand("{}", () =>
        commandCallback("{}")
    )
  );
"""


def create_extension_js(extension):
    with open(os.path.join(os.path.split(__file__)[0], "extension_code.js"), "r") as f1:
        imports, contents = f1.read().split("// func: registerCommands")

    file = os.path.split(inspect.stack()[-1].filename)[-1]
    imports = imports.replace("<filepath>", file)
    commands_code = "function registerCommands(context) {\n\t"
    for cmd in extension.commands:
        args = cmd.extension_string, cmd.name
        commands_code += REGISTER_COMMANDS_TEMPLATE.format(*args)

    commands_code += "\n}"

    with open("extension.js", "w") as f2:
        f2.write(f"{imports}\n{commands_code}\n{contents}")


def build(extension) -> None:
    print(f"\033[1;37;49m🚀 Building Extension '{extension.name}' ...", "\033[0m")
    start = time.time()

    if not os.path.isdir("./venv"):
        print(f"\033[1;37;49mSetting up the virtual environment...", "\033[0m")
        # venv.create("./venv", with_pip=True)

    create_launch_json()
    print(f"\033[1;37;49mCreating package.json...", "\033[0m")
    create_package_json(extension)

    print(f"\033[1;37;49mCreating extension.js...", "\033[0m")
    create_extension_js(extension)

    if not os.path.isdir("./node_modules/ws"):
        os.system("npm i ws --save-dev")

    end = time.time()
    time_taken = round((end - start) * 1000, 2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} ms! ✨", "\033[0m")
