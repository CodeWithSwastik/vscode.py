'''// Built using vscode-ext
const vscode = require("vscode");
const spawn = require("child_process").spawn;
const path = require("path");
const pythonPath = path.join(__dirname, "extension.py");
const requirements = path.join(__dirname, "../requirements.txt");
const osvar = process.platform;

if (osvar == "win32") {
  spawn("python", ["-m", "pip", "install", "-r", requirements]);
} else {
  spawn("python3", ["-m", "pip3", "install", "-r", requirements]);
}

function executeCommands(pythonProcess, data, globalStorage) {
  let ogdata = data.toString();
  data = ogdata.split("\n");
  let debug = data.slice(0, data.length - 1);
  data = data[data.length - 1];
  try {
    data = JSON.parse(data);
    code = data.code;
    if (!code) {
      throw Error;
    }
    args = data.args;
  } catch {
    return console.log("Debug message from extension.py: " + ogdata);
  }
  if (debug.length > 0) {
    console.log("Debug message from extension.py: " + debug);
  }
  switch (code) {
    case "SM":
      vscode.window[args[0]](...args.slice(1)).then((r) =>
        pythonProcess.stdin.write(JSON.stringify(r) + "\n")
      );
      break;
    case "QP":
      vscode.window
        .showQuickPick(args[0], args[1])
        .then((r) => pythonProcess.stdin.write(JSON.stringify(r) + "\n"));
      break;
    case "IB":
      vscode.window
        .showInputBox(args[0])
        .then((s) => pythonProcess.stdin.write(JSON.stringify(s) + "\n"));
      break;
    case "OE":
      vscode.env.openExternal(args[0]);
      break;
    case "EP":
      pythonProcess.stdin.write(JSON.stringify(vscode.env[args[0]]) + "\n");
      break;
    case "GC":
      pythonProcess.stdin.write(
        JSON.stringify(
          vscode.workspace.getConfiguration(args[0]).get(args[1])
        ) + "\n"
      );
      break;
    case "BM":
      let dis;
      if (args.length > 1) {
        dis = vscode.window.setStatusBarMessage(args[0], args[1]);
      } else {
        dis = vscode.window.setStatusBarMessage(args[0]);
      }
      let id = "id" + Math.random().toString(16).slice(2);
      globalStorage[id] = dis;
      pythonProcess.stdin.write(JSON.stringify(id) + "\n");
      break;
    case "DI":
      globalStorage[args[0]].dispose();
      break;
    case "AT":
      pythonProcess.stdin.write(
        JSON.stringify(vscode.window.activeTextEditor) + "\n"
      );
      break;
    case "GT":
      let editor = vscode.window.activeTextEditor;
      let res;
      if (!editor) {
        res = undefined;
      } else if (args.length > 0) {
        let { start, end } = JSON.parse(args[0]);
        let range = new vscode.Range(
          start.line,
          start.character,
          end.line,
          end.character
        );
        res = editor.document.getText(range);
      } else {
        res = editor.document.getText();
      }
      pythonProcess.stdin.write(JSON.stringify(res) + "\n");
      break;
    case "EE":
      let { start, end } = JSON.parse(args[0]);
      let range = new vscode.Range(
        start.line,
        start.character,
        end.line,
        end.character
      );
      if (!vscode.window.activeTextEditor) {
        return pythonProcess.stdin.write("undefined\n");
      }
      vscode.window.activeTextEditor
        .edit((editB) => {
          editB.replace(range, args[1]);
        })
        .then((s) => pythonProcess.stdin.write(JSON.stringify(s) + "\n"));
      break;
    case "LA":
      if (!vscode.window.activeTextEditor) {
        return pythonProcess.stdin.write("undefined\n");
      }
      let cline = vscode.window.activeTextEditor.document.lineAt(
        parseInt(args[0])
      );
      return pythonProcess.stdin.write(JSON.stringify(cline) + "\n");
    case "ST":
      vscode.window
        .showTextDocument(vscode.Uri.file(args[0]), args[1])
        .then((s) => pythonProcess.stdin.write(JSON.stringify(s) + "\n"));
      break;
    default:
      console.log("Couldn't parse this: " + data);
  }
}
'''