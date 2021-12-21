from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .extension import Extension

def create_package_json(data: dict, config: dict) -> dict:
    package_name = data["name"]
    package = {
        "name": package_name,
        "displayName": data.get("display_name", package_name),
        "version": data["version"],
        "engines": "^1.58.0",
        "categories": "Other",
        "main": "./build/extension.js",
    }
    package.update(config)
    return package

def build(extension: Extension) -> None:
    pass