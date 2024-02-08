#!/usr/bin/env python3

import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_project_root", type=str)
    args = parser.parse_args()

    target_project_root = args.target_project_root
    
    # update path
    bashrc_path = os.path.expanduser("~/.bashrc")
    os.system(f"echo '\nexport PATH=$PATH:{target_project_root}/bin # added by templates/python/init.py\n' >> {bashrc_path}")

    # install dependencies
    which_pip3 = subprocess.check_output(["which", "pip3"]).decode("utf-8").strip()
    if which_pip3 != "/opt/conda/bin/pip3":
        print("Expected installation to be happening in a conda environment.")
        exit(1)
    
    os.system(f"pip3 install -r {target_project_root}/requirements.txt")
    os.system(f"npm i")


if __name__ == "__main__":
    main()
