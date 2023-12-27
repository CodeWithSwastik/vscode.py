'''// Built using vscode.py
const vscode = require("vscode");
const { spawn, execSync } = require("child_process");
const path = require("path");
const pythonExtensionPath = path.join(__dirname, "extension.py");
const requirementsPath = path.join(__dirname, "requirements.txt");

const wslib = require("ws");
const fs = require("fs");
let ws;

function commandCallback(command) {
  if (ws && ws.readyState == 1) {
    ws.send(JSON.stringify({ type: 1, name: command }));
  } else {
    setTimeout(() => commandCallback(command), 50);
  }
}

// func: registerCommands

function activate(context) {
  registerCommands(context);

  let pyVar = process.platform == "win32" ? "python" : "python3";
  let venvPath = path.join(__dirname, "./venv");
  let createvenvPath = path.join(venvPath, "createvenv.txt");
  if (!fs.existsSync(createvenvPath)) {
    execSync(`${pyVar} -m venv ${venvPath}`);
    fs.writeFileSync(
      createvenvPath,
      "Delete this file only if you want to recreate the venv! Do not include this file when you package/publish the extension."
    );
  }

  pyVar = path.join(
    venvPath,
    process.platform == "win32" ? "Scripts/python.exe" : "bin/python"
  );
  execSync(`${pyVar} -m pip install -r ${requirementsPath}`);

  let py = spawn(pyVar, [pythonExtensionPath, "--run-webserver"]);
  let webviews = {};
  let progressRecords = {};

  py.stdout.on("data", (data) => {
    let mes = data.toString().trim();
    if (ws) {
      console.log(mes);
    }
    let arr = mes.split(" ");
    if (arr.length == 3 && arr[arr.length - 1].startsWith("ws://localhost:")) {
      ws = new wslib.WebSocket(arr[arr.length - 1]);
      console.log("Connecting to " + arr[arr.length - 1]);
      ws.on("open", () => {
        console.log("Connected!");
        ws.send(JSON.stringify({ type: 2, event: "activate" }));
      });
      ws.on("message", async (message) => {
        console.log("received: %s", message.toString());
        try {
          let data = JSON.parse(message.toString());
          if (data.type == 1) {
            eval(data.code);
          } else if (data.type == 2) {
            eval(
              data.code +
                `.then(res => ws.send(JSON.stringify({ type: 3, res, uuid: "${data.uuid}" })));`
            );
          } else if (data.type == 3) {
            let res = eval(data.code);
            ws.send(JSON.stringify({ type: 3, res, uuid: data.uuid }));
          }
        } catch (e) {
          console.log(e);
        }
      });

      ws.on("close", () => {
        console.log("Connection closed!");
      });
    }
  });
  py.stderr.on("data", (data) => {
    console.error(`An Error occurred in the python script: ${data}`);
  });
}

function deactivate() {}

module.exports = { activate, deactivate };
'''