# Publishing Extensions

In order to publish your extension created with vscode-ext you should build your extension with the publish flag as follows:

```py
vscode.build(ext, publish=True)
```

This will generate the `README.md` and `CHANGELOG.md` for your extension. It's important to keep these updated. It will also create the `.vscodeignore` file. The contents of this file will be removed from being packaged in your extension.

After this you have to follow the steps mentioned in the [official documentation for publishing extensions.](https://code.visualstudio.com/api/working-with-extensions/publishing-extension)
