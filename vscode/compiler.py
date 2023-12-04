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
        "dependencies": {
            "ws": "^8.4.0",
        }
    }
    metadata = extension.metadata.to_dict()
    package.update(metadata)

    if extension.keybindings:
        package["contributes"].update({"keybindings": extension.keybindings})

    if extension.config:
        package["contributes"]["configuration"] = {
                "title": extension.display_name,
                "properties":{
                    f"{extension.name}.{c.name}": c.to_dict() for c in extension.config
                }
            }
    

    cwd = os.getcwd()

    package_dir = os.path.join(cwd, "package.json")
    if os.path.isfile(package_dir):
        with open(package_dir, "r") as f:
            try:
                new_package = json.load(f)
                new_package.update(package)
            except json.decoder.JSONDecodeError:
                new_package = package
    else:
        new_package = package

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

def get_vsc_filepath(file):
    return os.path.join(os.path.split(__file__)[0], file)

def create_extension_js(extension):
    js_code_path = get_vsc_filepath("extcode.js")
    if os.path.isfile(js_code_path):
        with open(js_code_path, "r") as f:
            code = f.read()
    else:
        with open(get_vsc_filepath("extcode.py"), "r") as f:
            code = f.read().replace("'''", "")

    imports, contents = code.split("// func: registerCommands")

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

    if not os.path.isfile("requirements.txt"):
        print(f"\033[1;37;49mA requirements.txt wasn't found in this directory. If your extension has any dependencies kindly put them in the requirements.txt", "\033[0m")
        with open("requirements.txt", "w") as f:
            f.write("vscode.py==2.0.0a5")

    if not os.path.isdir("./venv"):
        print(f"\033[1;37;49mSetting up the virtual environment...", "\033[0m")
        venv.create("./venv", with_pip=True)

    print(f"\033[1;37;49mInstalling dependencies...", "\033[0m")
    python_path = os.path.join(os.getcwd(), "venv/Scripts/python.exe")
    if not os.path.exists(python_path):
        python_path = os.path.join(os.getcwd(), "venv/bin/python")
    os.system(f"{python_path} -m pip install -r requirements.txt")


    create_launch_json()
    print(f"\033[1;37;49mCreating package.json...", "\033[0m")
    create_package_json(extension)

    print(f"\033[1;37;49mCreating extension.js...", "\033[0m")
    create_extension_js(extension)

    if not os.path.isdir("./node_modules/ws"):
        os.system("npm i ws")

    end = time.time()
    time_taken = round((end - start), 2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} seconds! ✨", "\033[0m")
