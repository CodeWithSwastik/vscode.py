// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonExtensionPath = path.join(__dirname, "<filepath>");
const wslib = require("ws");
let ws;

function commandCallback(command) {
  if (ws && ws.readyState == 1) {
    ws.send(JSON.stringify({ type: 1, name: command }));
  } else {
    setTimeout(() => commandCallback(command), 100);
  }
}

// func: registerCommands

function activate(context) {
  console.log("Test has been activated");

  let pyVar = "python.exe";
  let py = spawn(pyVar, [pythonExtensionPath, "test"]);

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
        console.log("closed");
      });
    }
  });
  py.stderr.on("data", (data) => {
    console.error(`An Error occurred in the python script: ${data}`);
  });

  registerCommands(context);
}

function deactivate() {}

module.exports = { activate, deactivate };
