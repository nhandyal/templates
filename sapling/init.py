#!/usr/bin/env python3

import argparse
import os
import subprocess


def get_git_remote_url(target_project_root: str) -> str:
    # git remote -v returns something like the following:
    # origin  https://github.com/nhandyal/sapling_build.git (fetch)
    # origin  https://github.com/nhandyal/sapling_build.git (push)
    git_remote = subprocess.check_output("git remote -v", shell=True, cwd=target_project_root).decode("utf-8").strip()
    git_remote_url = git_remote.split("\n")[0].split()[1].strip()
    if "https" not in git_remote_url:
        raise ValueError(f"git remote url is not https: {git_remote_url}")
    
    return git_remote_url


def check_if_repo_exists_in_worspaces(target_project_root: str):
    repo_name = get_git_remote_url(target_project_root).split("/")[-1].replace(".git", "")
    if not os.path.exists(f"/workspaces/{repo_name}"):
        print(f"Error: /workspaces/{repo_name} does not exist.")
        print("This script is likely not being run inside a docker container. Exiting...")
        
        print("")
        raise ValueError(f"/workspaces/{repo_name} does not exist.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_project_root", type=str)
    args = parser.parse_args()

    target_project_root = args.target_project_root

    print("This script initializes Sapling SCM for")
    print(f"  {target_project_root}")
    print("")
    print("After this script, Git will be unavailable for this project.")
    print("")
    print("!!! WARNING !!!")
    print("This script clones the latest version of the repo using sapling")
    print("It then deletes the .git folder replacing it with the .sl folder.")
    print("")
    print("DO NOT USE THIS SCRIPT IF THERE ARE LOCAL CHANGES THAT HAVE NOT BEEN PUSHED.")
    print("THEY WILL IRRECOVERABLY LOST IF THEY AREN'T PUSHED AND YOU CONTINUE.")

    if input("Are you sure you want to continue? (y/n) ") != "y":
        print("Exiting...")
        exit(0)
    
    print("")
    print("")
    
    check_if_repo_exists_in_worspaces(target_project_root)
    git_remote_url = get_git_remote_url(target_project_root)
    commands = [
        f"sl clone {git_remote_url} /tmp/repo",
        "cp -r /tmp/repo/.sl /workspaces",
        "rm -rf /workspaces/.git /tmp/repo",
    ]
    for command in commands:
        subprocess.check_call(command, shell=True, cwd=target_project_root)
    

if __name__ == "__main__":
    main()