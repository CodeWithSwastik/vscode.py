import os
import time
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vscode.extension import Extension


def create_package_json(extension) -> None:
    package = {
        "name": extension.name,
        "displayName": extension.display_name,
        "version": "0.0.1",
        "engines": {"vscode": "^1.58.0"},
        "categories": ["Other"],
        "main": "./extension.js",
        "contributes": {
            "commands": [cmd.to_dict() for cmd in extension.commands],
        },
        "activationEvents": [
            "onCommand:" + cmd.extension_string for cmd in extension.commands
        ],
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
                new_package = package
    else:
        new_package = package
    with open(package_dir, "w") as f:
        json.dump(new_package, f, indent=2)


def build(extension) -> None:
    print(f"\033[1;37;49m🚀 Building Extension '{extension.name}' ...", "\033[0m")
    start = time.time()

    print(f"\033[1;37;49mCreating package.json...", "\033[0m")
    create_package_json(extension)

    print(f"\033[1;37;49mCreating extension.js...", "\033[0m")

    end = time.time()
    time_taken = round((end - start) * 1000, 2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} ms! ✨", "\033[0m")
