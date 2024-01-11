#!/usr/bin/env python3

import argparse
import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("init", type=str, choices=["sapling", "typescript"])
    args = parser.parse_args()

    # delete every file and directory in SCRIPT_DIR except for
    # ".git" and args.init
    for rel_path in os.listdir(SCRIPT_DIR):
        if rel_path == ".git" or rel_path == args.init:
            continue

        abs_path = os.path.join(SCRIPT_DIR, rel_path)
        if os.path.isdir(abs_path):
            # print(f"Deleting dir {abs_path}")
            shutil.rmtree(abs_path)
        elif os.path.isfile(abs_path):
            # print(f"Deleting file {abs_path}")
            os.remove(abs_path)
        else:
            raise Exception(f"Unknown type {abs_path}")
    
    # # copy everything in the args.init directory to this directory
    for rel_path in os.listdir(f"{SCRIPT_DIR}/{args.init}"):
        abs_path = os.path.join(SCRIPT_DIR, args.init, rel_path)
        copy_path = os.path.join(SCRIPT_DIR, rel_path)
        if os.path.isdir(abs_path):
            # print(f"Copying dir {abs_path} to {copy_path}")
            shutil.copytree(abs_path, copy_path)
        elif os.path.isfile(abs_path):
            # print(f"Copying file {abs_path} to {copy_path}")
            shutil.copy(abs_path, copy_path)
        else:
            raise Exception(f"Unknown type {abs_path}")
    
    # delete args.init
    shutil.rmtree(f"{SCRIPT_DIR}/{args.init}")


if __name__ == "__main__":
    main()
