import os
import json

def create_package(data, activation_events, commands):
    package_name = data["name"]
    package = {
        "name": package_name,
        "displayName": data.get("display_name",package_name),
        "description": data.get("description", ""),
        "version": data["version"],
        "engines": {
            "vscode": "^1.58.0"
        },
        "categories": [
            "Other"
        ],
        "activationEvents": activation_events,
        "main": "./build/extension.js",
        "contributes": {
            "commands": commands,
        },
    }
    return package


extensions_json = {
	"recommendations": [
		"dbaeumer.vscode-eslint"
	]
}

launch_json = {
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Run Extension",
      "type": "extensionHost",
      "request": "launch",
      "args": ["--extensionDevelopmentPath=${workspaceFolder}"]
    },
    {
      "name": "Extension Tests",
      "type": "extensionHost",
      "request": "launch",
      "args": [
        "--extensionDevelopmentPath=${workspaceFolder}",
        "--extensionTestsPath=${workspaceFolder}/test/suite/index"
      ]
    }
  ]
}

def build_js(name, events, commands):
    imports = "const vscode = require('vscode');\n"

    on_activate = events.get('activate')
    code_on_activate = 'function activate(context) {\n'   
    if on_activate:
        code_on_activate += f'console.log("{on_activate()}");\n'
    
    for command in commands:
        code_on_activate += f"let {command.name} = vscode.commands.registerCommand('{command.extension(name)}',"+' function () {\n'
        # It has been hardcoded for now!
        code_on_activate += f"vscode.window.showInformationMessage('{command.func()}');\n"
        code_on_activate += "});\n"
        code_on_activate += f"context.subscriptions.push({command.name});\n"+"}\n"

    on_deactivate = events.get('deactivate')
    code_on_deactivate = 'function deactivate() {'
    if on_deactivate:
        code_on_activate += f'\nconsole.log("{on_deactivate()}");\n'
    code_on_deactivate += '}'
    main = code_on_activate + '\n' + code_on_deactivate
    exports = 'module.exports = {activate,deactivate}'
    code = f'{imports}\n{main}\n\n{exports}'
    return code
def create_files(package, javascript):
    cwd = os.getcwd()

    # ---- Static ----

    vscode_path = os.path.join(cwd,'.vscode')
    os.makedirs(vscode_path, exist_ok=True)
    os.chdir(vscode_path)

    with open('extensions.json','w') as f:
        json.dump(extensions_json, f, indent=2)
    
    with open('launch.json','w') as f:
        json.dump(launch_json, f, indent=2)
    
    # ---- Static ----
    
    with open(os.path.join(cwd,'package.json'), 'w') as f:
        json.dump(package, f, indent=2)
    
    build_path = os.path.join(cwd,'build')
    os.makedirs(build_path, exist_ok=True)
    os.chdir(build_path)
    with open('extension.js','w') as f:
        f.write(javascript)

    os.chdir(cwd)

def build(extension):
    ext_data = extension.__dict__
    package_name = ext_data['name']

    commands = []
    activation_events = []
    for command in ext_data.get('commands'):
        cmd = {
            "command": f"{package_name}.{command.name}",
            "title": command.title            
        }
        event = 'onCommand:' + command.extension(package_name)
        commands.append(cmd)
        activation_events.append(event)
    package = create_package(ext_data, activation_events, commands)
    javascript = build_js(package_name, ext_data['events'], ext_data['commands'])
    create_files(package, javascript)
