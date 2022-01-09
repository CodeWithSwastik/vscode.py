import os
import time
import json
import venv
import inspect
from pathlib import Path

from vscode.extension import Launch

__all__ = ("build",)

COMMAND = {"title", "category", "command"}


def create_package_json(extension) -> None:
    package = {
        "name": extension.name,
        "displayName": extension.display_name,
        "main": "./extension.js",
        "contributes": {
            "commands": [
                cmd.dict(include=COMMAND, exclude_unset=True)
                for cmd in extension.commands
            ],
        },
        "activationEvents": ["onCommand:" + cmd.command for cmd in extension.commands],
        "dependencies": {
            "ws": "^8.4.0",
        },
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
            except json.decoder.JSONDecodeError:
                new_package = package
                new_package.update(first_info)
    else:
        new_package = package
        new_package.update(first_info)

    with open(package_dir, "w") as f:
        json.dump(new_package, f, indent=2)


def create_launch_json():

    vscode_path = Path.cwd().joinpath(".vscode")
    vscode_path.mkdir(exist_ok=True)

    with open(vscode_path.joinpath("launch.json"), "w") as f:
        f.write(Launch().json(indent=2))


REGISTER_COMMANDS_TEMPLATE = """
  context.subscriptions.push(
    vscode.commands.registerCommand("{command}", () =>
        commandCallback("{name}")
    )
  );
"""


def get_vsc_filepath(file):
    return Path(__file__).with_name(file)


def create_extension_js(extension):
    js_code_path = get_vsc_filepath("extcode.js")
    if js_code_path.exists():
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
        commands_code += REGISTER_COMMANDS_TEMPLATE.format(**cmd.dict())

    commands_code += "\n}"

    with open("extension.js", "w") as f2:
        f2.write(f"{imports}\n{commands_code}\n{contents}")


def build(extension) -> None:
    print(f"\033[1;37;49m🚀 Building Extension '{extension.name}' ...", "\033[0m")
    start = time.time()

    if not os.path.isfile("requirements.txt"):
        print(
            f"\033[1;37;49mA requirements.txt wasn't found in this directory. If your extension has any dependencies kindly put them in the requirements.txt",
            "\033[0m",
        )

        # TODO: Add websockets requirement
        with open("requirements.txt", "w") as f:
            f.write("git+https://github.com/CodeWithSwastik/vscode-ext@main")

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
        os.system("npm i ws --save-dev")

    end = time.time()
    time_taken = round((end - start), 2)
    print(
        f"\033[1;37;49mBuild completed successfully in {time_taken} seconds! ✨",
        "\033[0m",
    )
