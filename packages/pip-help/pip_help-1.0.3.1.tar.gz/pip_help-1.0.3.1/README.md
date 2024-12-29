# pip-help
pip-help is a command line tool for temporarily installing packages.

- **Source Code:** https://github.com/ilokeshpawar/pip-help
- **Bug reports:** https://github.com/ilokeshpawar/pip-help/issues

## Problem:
- It often happens that for some tasks, you have to install a `<package>` on your system. During that process, you end up downloading many `<dependent_packages>` which you might not require once the task is finished.

- When you uninstall the `<package>` using pip, the process only uninstalls the `<package>` and not the `<dependent_packages>`.

- Although you have uninstalled the `<package>`, the `<cache>` and `<dependent_packages>` remain somewhere on your system, taking up memory.

## Solution
- This tool aims to solve all the problems listed above.

## Installation Guide
- `pip install pip-help`

## Getting Started
Currently, it provides support for installing and uninstalling a single or multiple `<packages>`. let's consider that the package name is `"matplotlib"`and its <dependent_packages>.

- Use the flag `-h/--help` for further information.

- Example usage (installing a package): `pip-help -i (or --install) matplotlib`

- Example usage (uninstalling a package): `pip-help -r (or --remove) matplotlib`

## PS
- It can install and uninstall multiple packages in one go.
