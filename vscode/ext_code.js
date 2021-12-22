// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonPath = path.join(__dirname, "test.py");
let wslib = require("ws");

function activate(context) {
  console.log("Test has been activated");

  let pyVar = "python";
  let py = spawn(pyVar, [pythonPath, "test"]);

  py.stdout.on("data", (data) => {
    let mes = data.toString().trim();
    console.log(mes);
    let arr = mes.split(" ");
    if (arr.length == 3 && arr[arr.length - 1].startsWith("ws://localhost:")) {
      const ws = new wslib.WebSocket(arr[arr.length - 1]);
      ws.on("open", () => {
        console.log("Connected!");
        ws.send(JSON.stringify({ type: 1, name: "helloWorld" }));

        ws.on("message", async (message) => {
          console.log("received: %s", message.toString());
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

  let search = vscode.commands.registerCommand(
    "my-extension.helloWorld",
    async function () {}
  );
  context.subscriptions.push(search);
}

function deactivate() {}

module.exports = { activate, deactivate };
