#!/usr/bin/env python3

import argparse
import os
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def deep_merge(dict1, dict2):
    """
    Recursively merges dict2 into dict1
    """
    for key in dict2:
        if key in dict1:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                deep_merge(dict1[key], dict2[key])
            elif isinstance(dict1[key], list) and isinstance(dict2[key], list):
                dict1[key].extend(dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            dict1[key] = dict2[key]
    
    return dict1


def copy_dirs(target_project_root: str) -> None:
    dirs = [
        "bin",
        "python",
    ]

    for d in dirs:
        source_dir = os.path.join(SCRIPT_DIR, d)
        os.system(f"cp -r {source_dir} {target_project_root}")

    bashrc_path = os.path.expanduser("~/.bashrc")
    os.system(f"echo '\nexport PATH=$PATH:{target_project_root}/bin # added by templates/python/init.py\n' >> {bashrc_path}")


def copy_files(target_project_root: str) -> None:
    fies = [
        ".flake8",
        ".isort.cfg",
        "pyrightconfig.json",
        "pytest.ini",    
    ]
    for f in fies:
        os.system(f"cp {os.path.join(SCRIPT_DIR, f)} {target_project_root}")


def deep_merge_files(target_project_root: str) -> None:
    files = [
        ".devcontainer/devcontainer.json",
        ".vscode/launch.json",
        ".vscode/settings.json",
        ".gitignore",
        "requirements.txt",
        "package.json",
    ]

    for f in files:
        source_file = os.path.join(SCRIPT_DIR, f)
        target_file = os.path.join(target_project_root, f)
        target_dir = os.path.dirname(target_file)
        
        os.system(f"mkdir -p {target_dir}")

        if os.path.exists(target_file):
            pass
        else:
            os.system(f"cp {source_file} {target_file}")



        if os.path.exists(target_file):
            os.system(f"cat {source_file} >> {target_file}")
        else:
            os.system(f"cp {source_file} {target_file}")

def merge_gitignore(target_project_root: str) -> None:
    source_gitignore = os.path.join(SCRIPT_DIR, ".gitignore")
    target_gitignore = os.path.join(target_project_root, ".gitignore")
    if os.path.exists(target_gitignore):
        os.system(f"cat {source_gitignore} >> {target_gitignore}")
    else:
        os.system(f"cp {source_gitignore} {target_gitignore}")


def merge_vscode_settings(target_project_root: str) -> None:
    source_vscode_settings = os.path.join(SCRIPT_DIR, ".vscode", "settings.json")
    target_vscode_settings = os.path.join(target_project_root, ".vscode", "settings.json")
    
    if os.path.exists(target_vscode_settings):
        target_content = json.load(open(target_vscode_settings))
        source_content = json.load(open(source_vscode_settings))
        target_content = {**target_content, **source_content}
        json.dump(target_content, open(target_vscode_settings, "w"), indent=2)
    else:
        os.system(f"mkdir -p {os.path.dirname(target_vscode_settings)}")
        os.system(f"cp {source_vscode_settings} {target_vscode_settings}")


def merge_vscode_launch(target_project_root: str) -> None:
    source_vscode_launch = os.path.join(SCRIPT_DIR, ".vscode", "launch.json")
    target_vscode_launch = os.path.join(target_project_root, ".vscode", "launch.json")
    
    if os.path.exists(target_vscode_launch):
        target_content = json.load(open(target_vscode_launch))
        source_content = json.load(open(source_vscode_launch))
        
        target_content["configurations"] = target_content.get("configurations", []) + source_content.get("configurations", [])

        json.dump(target_content, open(target_vscode_launch, "w"), indent=2)
    else:
        os.system(f"mkdir -p {os.path.dirname(target_vscode_launch)}")
        os.system(f"cp {source_vscode_launch} {target_vscode_launch}")


def merge_devcontainer_json(target_project_root: str) -> None:
    source_devcontainer_json = os.path.join(SCRIPT_DIR, ".devcontainer", "devcontainer.json")
    target_devcontainer_json = os.path.join(target_project_root, ".devcontainer", "devcontainer.json")
    
    if os.path.exists(target_devcontainer_json):
        target_content = json.load(open(target_devcontainer_json))
        source_content = json.load(open(source_devcontainer_json))
        
        target_extensions = target_content.setdefault("customizations", {}).setdefault("vscode", {}).setdefault("extensions", [])
        source_extensions = source_content.setdefault("customizations", {}).setdefault("vscode", {}).setdefault("extensions", [])

        for i in source_extensions:
            if i not in target_extensions:
                target_extensions.append(i)

        json.dump(target_content, open(target_devcontainer_json, "w"), indent=2)
    else:
        os.system(f"mkdir -p {os.path.dirname(target_devcontainer_json)}")
        os.system(f"cp {source_devcontainer_json} {target_devcontainer_json}")


def install_requirements() -> None:
    which_pip3 = subprocess.check_output(["which", "pip3"]).decode("utf-8").strip()
    if which_pip3 != "/opt/conda/bin/pip3":
        print("Expected installation to be happening in a conda environment.")
        exit(1)
    
    os.system(f"pip3 install -r {SCRIPT_DIR}/requirements.txt")
    os.system(f"sudo npm install -g pyright")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", type=str, help="The target project to initialize into")
    args = parser.parse_args()

    target_project_root = f"/workspaces/{args.project_name}"
    
    if not os.path.exists(target_project_root):
        print(f"Error: {target_project_root} does not exist.")
        exit(1)
    
    if input(f"Initialize a python project in {target_project_root}? (y/n): ") != "y":
        exit(0)

    copy_dirs(target_project_root)
    copy_files(target_project_root)
    merge_gitignore(target_project_root)
    install_requirements()

    print("")
    print("FINISHED INITIALIZING PROJECT")
    print("init script may have overriden these files with customizations:")
    print("verify changes to:")
    print("  .gitignore")
    print("  .vscode/settings.json")
    print("  .vscode/launch.json")
    print("  .devcontainer/devcontainer.json")
    print("  requirements.txt")
    print("  package.json")
    


if __name__ == "__main__":
    main()
