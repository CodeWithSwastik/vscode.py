import os
import json
import time
import inspect
from .extension import Extension

def create_package(data, config):
    package_name = data["name"]
    package = {
        "name": package_name,
        "displayName": data.get("display_name", package_name),
        "version": data["version"],
        "engines": {"vscode": "^1.58.0"},
        "categories": ["Other"],
        "main": "./build/extension.js",
    }
    package.update(config)
    return package


extensions_json = {"recommendations": ["dbaeumer.vscode-eslint"]}

launch_json = {
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run Extension",
            "type": "extensionHost",
            "request": "launch",
            "args": ["--extensionDevelopmentPath=${workspaceFolder}"],
        },
        {
            "name": "Extension Tests",
            "type": "extensionHost",
            "request": "launch",
            "args": [
                "--extensionDevelopmentPath=${workspaceFolder}",
                "--extensionTestsPath=${workspaceFolder}/test/suite/index",
            ],
        },
    ],
}

pre_imports = """# Built using vscode-ext

import sys
"""


main_py = """
def ipc_main():
    globals()[sys.argv[1]]()

ipc_main()
"""


def build_py(functions):
    with open(inspect.getfile(functions[0]), "r") as f:
        imports = pre_imports + "".join([l for l in f.readlines() if not "build(" in l])
    imports += "\n"
    main = main_py
    code = imports + main
    return code


def build_js(name, events, commands, activity_bar_config=None):
    cwd = os.getcwd()
    python_path = os.path.join(cwd, "build", "extension.py").replace("\\", "\\\\")

    imports = ""
    directory, filename = os.path.split(inspect.getfile(build_py))
    with open(os.path.join(directory, "main.js"), "r") as f:
        imports += f.read()
    on_activate = events.get("activate")
    code_on_activate = "function activate(context) {\nlet globalStorage = {}\n"
    if on_activate:
        r = str(on_activate()).replace('"', '\\"')
        code_on_activate += f'console.log("{r}");\n'
    if activity_bar_config:
        html = activity_bar_config["html"].replace('"', '\\"')
        code_on_activate += (
            f'let html = "{html}"; let id = "{activity_bar_config["id"]}";\n'
        )
        code_on_activate += """
let thisProvider = {
  resolveWebviewView: function (thisWebview, thisWebviewContext, thisToken) {
    thisWebview.webview.options = { enableScript: true };
    thisWebview.webview.html = html;
  },
};
context.subscriptions.push(
  vscode.window.registerWebviewViewProvider(id, thisProvider)
);
            
            
"""
    for command in commands:
        code_on_activate += (
            f"let {command.name} = vscode.commands.registerCommand('{command.extension(name)}',"
            + "async function () {\n"
        )
        pyvar = "python" if os.name == 'nt' else 'python3'
        code_on_activate += (
            f'let funcName = "{command.func_name}"; let pyVar = "{pyvar}";'
        )
        code_on_activate += """
let py = spawn(pyVar, [pythonPath, funcName]);

py.stdout.on("data", (data) => {
    executeCommands(py, data, globalStorage);
});
py.stderr.on("data", (data) => {
    console.error(`An Error occurred in the python script: ${data}`);
});
"""
        code_on_activate += "});\n"
        code_on_activate += f"context.subscriptions.push({command.name});\n"

    code_on_activate += "}\n"

    on_deactivate = events.get("deactivate")
    code_on_deactivate = "function deactivate() {"
    if on_deactivate:
        r = str(on_deactivate()).replace('"', '\\"')
        code_on_activate += f'\nconsole.log("{r}");\n'
    code_on_deactivate += "}"
    main = code_on_activate + "\n" + code_on_deactivate
    exports = "module.exports = {activate,deactivate}"
    code = f"{imports}\n{main}\n\n{exports}"
    return code


def create_files(package, javascript, python, publish):
    cwd = os.getcwd()

    # ---- Static ----

    vscode_path = os.path.join(cwd, ".vscode")
    os.makedirs(vscode_path, exist_ok=True)
    os.chdir(vscode_path)

    with open("extensions.json", "w") as f:
        json.dump(extensions_json, f, indent=2)

    with open("launch.json", "w") as f:
        json.dump(launch_json, f, indent=2)

    # ---- Dynamic ----
    package_dir = os.path.join(cwd, "package.json")
    if os.path.isfile(package_dir):
        with open(package_dir, "r") as f:
            try:
                existing = json.load(f)
                existing.update(package)
            except json.decoder.JSONDecodeError:
                existing = package
    else:
        existing = package
    with open(package_dir, "w") as f:
        json.dump(existing, f, indent=2)

    build_path = os.path.join(cwd, "build")
    os.makedirs(build_path, exist_ok=True)
    os.chdir(build_path)
    with open("extension.js", "w") as f:
        f.write(javascript)

    with open("extension.py", "w") as f:
        f.write(python)
    os.chdir(cwd)

    if not os.path.isfile("requirements.txt"):
        with open("requirements.txt", "w") as f:
            f.write("vscode-ext")

    if publish:
        if not os.path.isfile("README.md"):
            with open("README.md", "w") as f:
                pass

        if not os.path.isfile("CHANGELOG.md"):
            with open("CHANGELOG.md", "w") as f:
                pass

        if not os.path.isfile(".vscodeignore"):
            with open(".vscodeignore", "w") as f:
                f.write(".vscode/**")



def build(extension: Extension, publish:bool=False, config:dict=None) -> None:
    """
    Builds the extension. 
    """
    if config is None:
        config = {}
    if publish:
        if extension.publisher is None:
            config["publisher"] = input("Enter publisher name: ")
        else:
            config["publisher"] = extension.publisher 
        
    print(f"\033[1;37;49mBuilding Extension {extension.name}...", "\033[0m")
    start = time.time()

    ext_data = extension.__dict__
    package_name = ext_data["name"]

    commands = []
    activation_events = []
    for command in ext_data.get("commands"):
        cmd = {"command": f"{package_name}.{command.name}", "title": command.title}
        if command.category is not None:
            cmd.update({"category": command.category})
        event = "onCommand:" + command.extension(package_name)
        commands.append(cmd)
        activation_events.append(event)

    package_config = config
    package_config.update(
        {
            "contributes": {
                "commands": commands,
            },
            "activationEvents": activation_events,
        }
    )

    if extension.keybindings:
        package_config["contributes"].update({"keybindings": extension.keybindings})

    if extension.activity_bar:
        package_config["contributes"]["viewsContainers"] = {
            "activitybar": [extension.activity_bar]
        }
        bar = extension.activity_bar
        webview = extension.activity_bar_webview
        view = {
            extension.activity_bar["id"]: [
                {
                    "id": f'{extension.name}.{bar["id"]}'
                    if not webview
                    else webview["id"],
                    "name": webview["title"]
                    if webview and webview["title"]
                    else bar["title"],
                }
            ]
        }
        if extension.activity_bar_webview:
            view[extension.activity_bar["id"]][0].update({"type": "webview"})
            package_config["activationEvents"].append(
                f"onView:{extension.activity_bar_webview['id']}"
            )
        if "views" in package_config["contributes"]:
            package_config["contributes"]["views"].update(view)
        else:
            package_config["contributes"]["views"] = view
    if extension.description:
        package_config["description"] = extension.description
    if extension.icon:
        package_config["icon"] = extension.icon
    if extension.repository:
        package_config["repository"] = extension.repository

    package = create_package(ext_data, package_config)
    javascript = build_js(
        package_name,
        ext_data["events"],
        ext_data["commands"],
        extension.activity_bar_webview,
    )
    python = build_py([c.func for c in ext_data["commands"]])
    create_files(package, javascript, python, publish)
    end = time.time()
    time_taken = round((end - start) * 1000, 2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} ms!", "\033[0m")
