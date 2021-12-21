import os
import time
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vscode.extension import Extension


def create_package_json(data: dict) -> dict:
    package_name = data["name"]
    package = {
        "name": package_name,
        "displayName": data.get("display_name", package_name),
        "version": "0.0.1",
        "engines": {
            "vscode": "^1.58.0"
        },
        "categories": ["Other"],
        "main": "./build/extension.js",
    }
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
    create_package_json(extension.__dict__)

    print(f"\033[1;37;49mCreating extension.js...", "\033[0m")

    end = time.time()
    time_taken = round((end - start) * 1000, 2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} ms! ✨", "\033[0m")
