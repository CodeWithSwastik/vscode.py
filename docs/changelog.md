# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- No errors being logged when there is an error in the js file.

### Deprecated

- `vscode.ext` has now been deprecated and will be removed by 1.6.0, all of the ext functions/classes can now be accessed through `vscode` directly.

## [1.5.3] - 2021-08-01

### Added

- vscode.window.show_text_document
- context managers with vscode.window.set_status_bar_message

## [1.5.2] - 2021-07-31

### Added

- This CHANGELOG file
- Workspace Configurations
- Documentation

### Fixed

- main.js not being included in packages
