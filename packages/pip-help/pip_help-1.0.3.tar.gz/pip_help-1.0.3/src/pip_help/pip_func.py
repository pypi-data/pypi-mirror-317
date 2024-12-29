import subprocess
import os
from pathlib import Path
from typing import TypeVar
import requests


def log_dest_path() -> Path:
    log_dest_path = os.path.join(os.path.expanduser("~"), "pip_help_logs")
    if not os.path.exists(log_dest_path):
        os.makedirs(log_dest_path)
    with open(f"{log_dest_path}/readme.md", "w") as file:
        file.write(
            "This directory contains logs of all the packages installed and removed using the pip-help command. Remove this directory if you are not using the pip-help command anymore."
        )
    return log_dest_path


File = TypeVar("File", str, Path)


def install(pip_package: str) -> None:
    log_path = os.path.join(log_dest_path(), f"pip_{pip_package}.txt")
    package = subprocess.call(
        ["pip", "install", pip_package, "--log", log_path, "--quiet"]
    )
    return package


def installed_packages_list(pip_package: str) -> File:
    target_path = os.path.join(log_dest_path(), f"pip_{pip_package}.txt")
    validation = False
    with open(target_path, "r") as file:
        possible_packages = []
        dependent_packages = []

        for line in file.readlines():
            target_line = line.lower().split(" ")
            word = "installing"
            if word in target_line:
                possible_packages.append(target_line)
        file.close()

        if len(possible_packages) == 0:
            print("-" * 66)
            print(
                f'WARINING: Package {pip_package.upper()} is already installed. it is recommended to uninstall "{pip_package}" and related packages before installing it again. To uninstall "{pip_package}" and related packages, run the command: \'pip-help --remove/-r {pip_package}\''
            )
            os.remove(target_path)

        else:
            for i, k in enumerate(possible_packages[0]):
                if k == "packages:":
                    target_packages = possible_packages[0][i + 1 :]
                    for target in target_packages:
                        package_name = target.strip().split(",")[0]
                        dependent_packages.append(package_name)
            print(f"{dependent_packages[-1]} is successfully installed!")

            with open((log_dest_path() + f"/pip_{pip_package}_list.txt"), "w") as file:
                try:
                    for pkg in dependent_packages:
                        file.write(f"{pkg}\n")
                        validation = True
                except Exception as e:
                    print(f"Error: {e}")

                if validation:
                    try:
                        os.remove(target_path)
                    except PermissionError as e:
                        print(
                            f"Error: {e}. Please close the file and try again to remove the file."
                        )


def uninstall(pip_package: str) -> None:
    log_path = log_dest_path() + f"/pip_{pip_package}_list.txt"
    if not os.path.exists(log_path):
        raise TypeError(
            f"The package {pip_package.upper()}, you are trying to remove is not installed."
        )
    else:
        package_uninstalled = subprocess.call(
            ["pip", "uninstall", "-r", log_path, "--yes"]
        )
        return package_uninstalled


def delete_pip_cache() -> None:
    clear_cache = subprocess.call(["pip", "cache", "purge"])
    return clear_cache


def pkg_on_pypi(pip_package: str) -> bool:
    request_api = requests.get(f"https://pypi.org/pypi/{pip_package}/json/")
    response = request_api.status_code
    if response == 200:
        return True
    else:
        return False
