#!/usr/bin/env python3

import argparse
import os
import subprocess
from pathlib import Path

CPU_ARCH_REMAP = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
}
CPU_ARCH = CPU_ARCH_REMAP[os.uname().machine]

DEVCONTAINER_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.realpath(os.path.join(DEVCONTAINER_DIR, ".."))


def main():
  build_directories =  [d for d in os.listdir('.') if os.path.isdir(d) and d != ".devcontainer"]

  parser = argparse.ArgumentParser(description="Build script for docker images")
  parser.add_argument("image_directory", choices=build_directories, help="The image directory to build")
  parser.add_argument("--push", action="store_true", help="Push the image to docker hub")
  args = parser.parse_args()

  if args.push:
    subprocess.check_call(f"docker login", shell=True)
  
  image_directory = os.path.join(DEVCONTAINER_DIR, args.image_directory)
  relative_build_context_path = Path(os.path.join(image_directory, "build_context.txt"))
  if not os.path.isfile(relative_build_context_path):
    print(f"Build context file {relative_build_context_path} not found")
    exit(1)
  
  abs_dockerfile = os.path.realpath(os.path.join(image_directory, "Dockerfile"))
  abs_build_context = os.path.join(ROOT_DIR, relative_build_context_path.read_text().strip())
  image_name = f"nhandyal/images:{args.image_directory}_{CPU_ARCH}"
  
  build_cmd = f"docker build -f {abs_dockerfile} -t {image_name} {abs_build_context}"
  print(f"Building image {image_name}")
  print(build_cmd)
  print("")
  # prompt the user to continue, exit if not y
  if input("Do you want to continue? (y/n) ") != "y":
    exit(0)

  subprocess.check_call(build_cmd, shell=True)

  if args.push:
    print(f"Pushing image {image_name} to docker hub")
    subprocess.check_call(f"docker push {image_name}", shell=True)


if __name__ == "__main__":
  main()
