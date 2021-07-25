import os
import json
import time
import inspect

def create_package(data, activation_events, commands):
    package_name = data["name"]
    package = {
        "name": package_name,
        "displayName": data.get("display_name", package_name),
        "description": data.get("description", ""),
        "version": data["version"],
        "engines": {"vscode": "^1.58.0"},
        "categories": ["Other"],
        "activationEvents": activation_events,
        "main": "./build/extension.js",
        "contributes": {
            "commands": commands,
        },
    }
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

main_py = '''\n
def ipc_main():
    globals()[sys.argv[1]]()

ipc_main()
'''

def build_py(functions):
    pre = '# Built using vscode-ext\n\n'
    with open(inspect.getfile(functions[0]), 'r') as f:
        imports = pre + ''.join([l for l in f.readlines() if not '.build(' in l])
    imports += "\nimport sys \n"
    main = main_py
    code = imports+main
    return code

def build_js(name, events, commands):
    cwd = os.getcwd()
    python_path = os.path.join(cwd, "build", "extension.py").replace('\\', '\\\\')
    pre = '// Built using vscode-ext\n\n'

    imports = pre + "const vscode = require('vscode');\nconst spawn = require('child_process').spawn;\n"

    on_activate = events.get("activate")
    code_on_activate = "function activate(context) {\n"
    if on_activate:
        code_on_activate += f'console.log("{on_activate()}");\n'

    for command in commands:
        code_on_activate += (
            f"let {command.name} = vscode.commands.registerCommand('{command.extension(name)}',"
            + " function () {\n"
        )
        code_on_activate += f'let pythonProcess = spawn("python", ["{python_path}","{command.func_name}"]);\n'
        code_on_activate += 'pythonProcess.stdout.on("data", (data) => {\n'
        code_on_activate += 'data = data.toString(); code = data.slice(0,2); args = data.substring(4).split("|||");\n'
        code_on_activate += 'if (code === "IM") {\n'
        code_on_activate += (
            f"vscode.window.showInformationMessage(...args);\n"
        )
        code_on_activate += "}\n"
        code_on_activate += "});\n"
        code_on_activate += "});\n"
        code_on_activate += f"context.subscriptions.push({command.name});\n"

    code_on_activate += "}\n"

    on_deactivate = events.get("deactivate")
    code_on_deactivate = "function deactivate() {"
    if on_deactivate:
        code_on_activate += f'\nconsole.log("{on_deactivate()}");\n'
    code_on_deactivate += "}"
    main = code_on_activate + "\n" + code_on_deactivate
    exports = "module.exports = {activate,deactivate}"
    code = f"{imports}\n{main}\n\n{exports}"
    return code


def create_files(package, javascript, python):
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

    with open(os.path.join(cwd, "package.json"), "w") as f:
        json.dump(package, f, indent=2)

    build_path = os.path.join(cwd, "build")
    os.makedirs(build_path, exist_ok=True)
    os.chdir(build_path)
    with open("extension.js", "w") as f:
        f.write(javascript)

    with open("extension.py", "w") as f:
        f.write(python)
    os.chdir(cwd)


def build(extension):
    print(f"\033[1;37;49mBuilding Extension...", "\033[0m")
    start = time.time()

    ext_data = extension.__dict__
    package_name = ext_data["name"]

    commands = []
    activation_events = []
    for command in ext_data.get("commands"):
        cmd = {"command": f"{package_name}.{command.name}", "title": command.title}
        event = "onCommand:" + command.extension(package_name)
        commands.append(cmd)
        activation_events.append(event)
    package = create_package(ext_data, activation_events, commands)
    javascript = build_js(package_name, ext_data["events"], ext_data["commands"])
    python = build_py([c.func for c in ext_data["commands"]])
    create_files(package, javascript, python)

    end = time.time()
    time_taken = round((end - start) * 1000,2)
    print(f"\033[1;37;49mBuild completed successfully in {time_taken} ms!", "\033[0m")
