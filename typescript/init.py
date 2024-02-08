#!/usr/bin/env python3

import argparse
import os
import subprocess

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_project_root", type=str)
    args = parser.parse_args()

    target_project_root = args.target_project_root

    # install dependencies
    subprocess.check_call(f"npm i", cwd=target_project_root, shell=True)


if __name__ == "__main__":
    main()
