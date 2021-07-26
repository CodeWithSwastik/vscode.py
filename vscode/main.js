// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonPath = path.join(__dirname, "extension.py");

function executeCommands(pythonProcess, data) {
  data = data
    .toString()
    .split("\n")
    .filter((e) => e !== "");
  debug = data.slice(0, data.length - 1);
  data = data[data.length - 1];
  code = data.slice(0, 2);
  args = data.substring(4).split("|||");
  switch (code) {
    case "SM":
      vscode.window[args[0]](...args.slice(1)).then((r) =>
        pythonProcess.stdin.write(r + "\n")
      );
      break;
    case "QP":
      vscode.window
        .showQuickPick(JSON.parse(args[0]), JSON.parse(args[1]))
        .then((r) => pythonProcess.stdin.write(JSON.stringify(r) + "\n"));
      break;
    case "OE":
      vscode.env.openExternal(args[0]);
      break;
    case "EP":
      pythonProcess.stdin.write(vscode.env[args[0]] + "\n");
      break;
    default:
      console.log("Couldn't parse this: " + data);
  }

  if (debug.length > 0) {
    console.log("Debug message from extension.py: " + debug);
  }
}