#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import subprocess

DEVCONTAINER_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.realpath(os.path.join(DEVCONTAINER_DIR, ".."))
BUILDER_NAME = "buildx_builder"

"""
## Building Multi-Architecture Docker Images with Docker Buildx

Follow these steps to build Docker images for multiple architectures using Docker Buildx:

1. **Ensure Docker Buildx is Available**
   - Docker Buildx comes with Docker 19.03+. 
   - Verify with `docker buildx version`.

2. **Create a New Builder Instance**
   - Create and switch to a new Buildx builder instance:
     ```
     docker buildx create --name mybuilder --use
     ```

3. **Start the Builder Instance**
   - Start and inspect the builder instance:
     ```
     docker buildx inspect --bootstrap
     ```

4. **Enable Experimental Features (If Required)**
   - Ensure Docker's experimental features are enabled, either in Docker's settings or by setting `DOCKER_CLI_EXPERIMENTAL=enabled` in your environment.

5. **Build and Push the Image**
   - Build your image for the desired platforms and push to a registry:
     ```
     docker buildx build --platform linux/amd64,linux/arm64 -t yourusername/yourimagename:tag --push .
     ```
   - Replace `yourusername/yourimagename:tag` with your actual image details.

6. **Verify the Image**
   - Verify the built image and its architectures:
     ```
     docker buildx imagetools inspect yourusername/yourimagename:tag
     ```

Note: Switching back to the "default" builder is not necessary unless specifically required for your workflow.

"""

class BuildConfig:
  def __init__(self, build_context, dockerfile, image_name, push, yes):
    self.build_context = build_context
    self.dockerfile = dockerfile
    self.image_name = image_name
    self.push = push
    self.yes = yes


def assert_git_clean():
  try:
    subprocess.check_call("git diff --exit-code > /dev/null", shell=True)
    subprocess.check_call("git diff --cached --exit-code > /dev/null", shell=True)
  except Exception:
    print("!! You must be in a clean git repository !!")
    print("Aborting ...")
    exit(1)
  
def get_head_rev():
  return subprocess.check_output("git rev-parse --short HEAD", shell=True).decode("utf-8").strip()

def main():
  build_directories =  [d for d in os.listdir('.') if os.path.isdir(d) and d != ".devcontainer"]

  parser = argparse.ArgumentParser(description="Build script for docker images")
  parser.add_argument("image_directory", choices=build_directories, help="The image directory to build")
  parser.add_argument("--push", action="store_true", help="Push the image to docker hub")
  parser.add_argument("--yes", action="store_true", help="Don't prompt for build confirmation")
  args = parser.parse_args()

  assert_git_clean()
  
  image_directory = os.path.join(DEVCONTAINER_DIR, args.image_directory)
  relative_build_context_path = Path(os.path.join(image_directory, "build_context.txt"))
  if not os.path.isfile(relative_build_context_path):
    print(f"Build context file {relative_build_context_path} not found")
    exit(1)
  
  multi_arch_build(BuildConfig(
    build_context=os.path.normpath(os.path.join(ROOT_DIR, relative_build_context_path.read_text().strip())),
    dockerfile=os.path.normpath(os.path.realpath(os.path.join(image_directory, "Dockerfile"))), 
    image_name=f"nhandyal/{args.image_directory}",
    push=args.push,
    yes=args.yes,
  ))
  
  
def multi_arch_build(build_config):
    push_or_load = "push" if build_config.push else "load"
    build_command = "\n".join([
      f"docker buildx build \\",
      f"  --builder {BUILDER_NAME} \\",
      f"  --platform linux/amd64,linux/arm64 \\",
      f"  --{push_or_load} \\",
      f"  -t {build_config.image_name}:{get_head_rev()} \\",
      f"  -t {build_config.image_name}:latest \\",
      f"  -f {build_config.dockerfile} \\",
      f"  {build_config.build_context}"
    ])

    print("The following will be built:")
    print(build_command)
    print("")

    if not build_config.yes:
      if input("Do you want to continue? (y/n) ") != "y":
        exit(0)
      
    if build_config.push:
      subprocess.check_call(f"docker login", shell=True)

    # enable QEMU for arm64 / amd64 emulataion
    subprocess.check_call("docker run --privileged --rm tonistiigi/binfmt --install all", shell=True)

    # Configure the builder
    try:
      subprocess.check_call(f"docker buildx inspect {BUILDER_NAME}", shell=True)
      # builder exists
    except Exception:
       # builder doesn't exist
       subprocess.check_call(f"docker buildx create --name {BUILDER_NAME} --driver docker-container --use", shell=True)
       subprocess.check_call(f"docker buildx inspect {BUILDER_NAME} --bootstrap", shell=True)

    # build the images
    subprocess.check_call(build_command, shell=True)


if __name__ == "__main__":
  main()
