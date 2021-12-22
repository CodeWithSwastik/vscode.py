// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonPath = path.join(__dirname, "test.py");
const wslib = require("ws");

let ws;

function activate(context) {
  console.log("Test has been activated");

  let pyVar = "python";
  let py = spawn(pyVar, [pythonPath, "test"]);

  py.stdout.on("data", (data) => {
    let mes = data.toString().trim();
    console.log(mes);
    let arr = mes.split(" ");
    if (arr.length == 3 && arr[arr.length - 1].startsWith("ws://localhost:")) {
      ws = new wslib.WebSocket(arr[arr.length - 1]);
      ws.on("open", () => {
        console.log("Connected!");

        ws.on("message", async (message) => {
          console.log("received: %s", message.toString());
          vscode.window.showInformationMessage(message.toString());
        });

        ws.on("close", () => {
          console.log("closed");
        });
      });
    }
  });
  py.stderr.on("data", (data) => {
    console.error(`An Error occurred in the python script: ${data}`);
  });
  async function commandCallback(command) {
    if (ws && ws.readyState == 1) {
      ws.send(JSON.stringify({ type: 1, name: command }));
    } else {
      setTimeout(() => commandCallback(command), 100);
    }
  }

  let search = vscode.commands.registerCommand("my-extension.helloWorld", () =>
    commandCallback("helloWorld")
  );
  context.subscriptions.push(search);
}

function deactivate() {}

module.exports = { activate, deactivate };
