import argparse
import os
import shutil


from pip_help.pip_func import (
    install,
    installed_packages_list,
    uninstall,
    delete_pip_cache,
    log_dest_path,
    pkg_on_pypi,
)


def get_args():
    parser = argparse.ArgumentParser(
        prog="pip help",
        description="Provide support for installing packages and dependendable packages temporarily.",
        epilog="If you followed the steps above, you have succesfully made your system cleaner and more efficient.",
    )
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "--install",
        "-i",
        type=str,
        help="The name of the package you want to install.",
        nargs="+",
    )
    group.add_argument(
        "--remove",
        "-r",
        type=str,
        help="The name of the package you want to remove.",
        nargs="+",
    )
    return parser.parse_args()


def main():
    args = get_args()
    package_install = args.install
    package_remove = args.remove

    if package_install:
        for package in package_install:
            pkg_exist = pkg_on_pypi(package)
            if pkg_exist is True:
                try:
                    print("*" * 66)
                    print(f"Installing {package}...")
                    install(package)
                except TypeError as e:
                    print(f"Error: {e}")
                finally:
                    installed_packages_list(package)
            else:
                print("*" * 66)
                print(
                    f"WARNING: Make sure {package} is a valid package name. Please try again."
                )
            print(
                f"NOTE!: {package} is not a valid package name."
                if not pkg_exist
                else ""
            )
    else:
        if package_remove:
            for package in package_remove:
                try:
                    print("*" * 45)
                    uninstall(package)
                    print("*" * 45)
                    cache = input(
                        "Do you want to delete the pip cache? (y/n): "
                    ).lower()
                    while cache not in ["y", "n"]:
                        cache = input(
                            "Please enter a valid input. Do you want to delete the pip cache? (y/n): "
                        ).lower()
                    if cache == "y":
                        delete_pip_cache()
                        os.remove((log_dest_path() + f"/pip_{package}_list.txt"))
                    else:
                        pass

                except TypeError as e:
                    print(f"Error: {e}")
        else:
            print(
                'WARNING: No argument provided. Please provide an argument. Use "--help/-h" for more information.'
            )

        if os.path.exists(log_dest_path()):
            if len(os.listdir(log_dest_path())) == 1:
                shutil.rmtree(log_dest_path())
            else:
                pass


if __name__ == "__main__":
    main()
