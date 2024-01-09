#!/usr/bin/env python3

import os
import subprocess


def get_git_remote_url():
    # git remote -v returns something like the following:
    # origin  https://github.com/nhandyal/sapling_build.git (fetch)
    # origin  https://github.com/nhandyal/sapling_build.git (push)
    git_remote = subprocess.check_output("git remote -v", shell=True).decode("utf-8").strip()
    git_remote_url = git_remote.split("\n")[0].split()[1].strip()
    if "https" not in git_remote_url:
        raise ValueError(f"git remote url is not https: {git_remote_url}")
    
    return git_remote_url


def check_if_repo_exists_in_worspaces():
    repo_name = get_git_remote_url().split("/")[-1].replace(".git", "")
    if not os.path.exists(f"/workspaces/{repo_name}"):
        print(f"Error: /workspaces/{repo_name} does not exist.")
        print("This script is likely not being run inside a docker container. Exiting...")
        
        print("")
        raise ValueError(f"/workspaces/{repo_name} does not exist. This script is likely not being run inside a docker container. Exiting...")


def main():
    print("This script initializes Sapling SCM for this container.")
    print("Initialization must be done on each container using Sapling.")
    print(
        "After running this script, you will no longer be able to use Git on this container."
    )
    print("")
    print("!!! WARNING !!!")
    print("This script clones the latest version of the repo using sapling")
    print("It then deletes the .git folder replacing it with the .sl folder.")
    print("")
    print("DO NOT USE THIS SCRIPT IF THERE ARE LOCAL CHANGES THAT HAVE NOT BEEN PUSHED.")
    print("THEY WILL IRRECOVERABLY LOST THEY AREN'T PUSHED AND YOU CONTINUE.")

    i = input("Are you sure you want to continue? (y/n) ")
    if i != "y":
        print("Exiting...")
        return
    
    print("")
    print("")
    
    check_if_repo_exists_in_worspaces()
    git_remote_url = get_git_remote_url()
    commands = [
        f"sl clone {git_remote_url} /tmp/repo",
        "cp -r /tmp/repo/.sl /workspaces",
        "rm -rf /workspaces/.git /tmp/repo",
    ]
    for command in commands:
        subprocess.check_call(command, shell=True)
    

if __name__ == "__main__":
    main()