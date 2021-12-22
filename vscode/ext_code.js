// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonPath = path.join(__dirname, "test.py");

function activate(context) {
  console.log("Test has been activated");

  let pyVar = "python";
  let py = spawn(pyVar, [pythonPath, "test"]);

  py.stdout.on("data", (data) => {
    console.log(data.toString());
    let arr = data.toString().trim().split(" ");
    if (arr[arr.length - 1].startsWith("ws://localhost:")) {
      console.log("Found ws");
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
