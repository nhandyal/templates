#!/usr/bin/env python3

import os
import shutil
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEV_CONTAINER_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

GITCONFIG_TEMPLATE = """
[user]
    name = {user_name}
    email = {user_email}
"""

SLCONFIG_TEMPLATE = """
[ui]
# name and email, e.g.
# username = Jane Doe <jdoe@example.com>
username = {user_name} <{user_email}>
"""


def main():
    try:
        git_user_name = subprocess.check_output("git config user.name", shell=True).decode().strip()
        git_user_email = subprocess.check_output("git config user.email", shell=True).decode().strip()

        with open(f"{DEV_CONTAINER_DIR}/configs/gitconfig", "r") as infile:
            with open(f"{DEV_CONTAINER_DIR}/generated/gitconfig", "w") as outfile:
                gitconfig = infile.read() + GITCONFIG_TEMPLATE.format(
                    user_name=git_user_name,
                    user_email=git_user_email,
                )
                outfile.write(gitconfig)
                print(f"Generated: {DEV_CONTAINER_DIR}/generated/gitconfig")

        with open(f"{DEV_CONTAINER_DIR}/configs/slconfig", "r") as infile:
            with open(f"{DEV_CONTAINER_DIR}/generated/slconfig", "w") as outfile:
                slconfig = infile.read() + SLCONFIG_TEMPLATE.format(
                    user_name=git_user_name,
                    user_email=git_user_email,
                )

                outfile.write(slconfig)
                print(f"Generated: {DEV_CONTAINER_DIR}/generated/slconfig")

    except subprocess.CalledProcessError:
        # unable to get user name and email from git config
        # copy the static config files to generated to.
        shutil.copyfile(f"{DEV_CONTAINER_DIR}/configs/gitconfig", f"{DEV_CONTAINER_DIR}/generated/gitconfig")
        shutil.copyfile(f"{DEV_CONTAINER_DIR}/configs/slconfig", f"{DEV_CONTAINER_DIR}/generated/slconfig")


if __name__ == "__main__":
    main()