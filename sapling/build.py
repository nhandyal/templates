#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import shutil
import subprocess


CPU_ARCH_REMAP = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
}

CPU_ARCH = CPU_ARCH_REMAP[os.uname().machine]
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
ARTIFACTS_DIR = f"{SCRIPT_DIR}/artifacts"
SAPLING_DIR = f"{ARTIFACTS_DIR}/sapling"

# The context for the build is the sapling repo root.
# We copy the locale folder into sapling after cloning it.
#
# This is to maintian interop with the sapling dockerfile
# which assumes the context is the sapling repo root.
DOCKERFILE_SAPLING_BUILD = """

RUN mkdir -p /tmp/repo/sapling
COPY . /tmp/repo/sapling

# Build Sapling
RUN cp /tmp/repo/sapling/nrh/build_deb.py /tmp/repo/sapling/eden/scm/packaging/debian/build_deb.py && \
    chmod +x /tmp/repo/sapling/eden/scm/packaging/debian/build_deb.py && \
    sed -i 's|./packaging/debian/build_deb.sh|./packaging/debian/build_deb.py|' /tmp/repo/sapling/eden/scm/Makefile && \
    cd /tmp/repo/sapling/eden/scm && \
    make deb && \
    mv sapling_*.deb /tmp/sapling.deb

FROM ubuntu:20.04 as final
COPY --from=0 /tmp/sapling.deb /tmp/sapling.deb
COPY --from=0 /tmp/repo/sapling/nrh/locale.gen /etc/locale.gen
COPY --from=0 /tmp/repo/sapling/nrh/default_locale /etc/default/locale

###########################
# Install locales
RUN apt-get update -y && \
    apt-get install -y ca-certificates curl git gnupg sudo vim wget locales

RUN dpkg -i ./tmp/sapling.deb
RUN locale-gen

CMD ["sl"]
"""


def build():
    if not os.path.exists(ARTIFACTS_DIR):
        os.mkdir(ARTIFACTS_DIR)

    if not os.path.exists(SAPLING_DIR):
        subprocess.check_call("gh repo clone facebook/sapling", shell=True, cwd=ARTIFACTS_DIR)
    
    # copy custom files into the sapling repo
    shutil.copytree(f"{SCRIPT_DIR}/locale", f"{SAPLING_DIR}/nrh", dirs_exist_ok=True)
    shutil.copy(f"{SCRIPT_DIR}/build_deb.py", f"{SAPLING_DIR}/nrh/build_deb.py")

    #############################
    # - copy the official dockerfile to a temp dockerfile 
    # - append build and bundle commands so that sapling is built into the image
    dockerfile_sapling_build_contents = Path(f"{SAPLING_DIR}/.github/workflows/sapling-cli-ubuntu-20.04.Dockerfile").read_text() + DOCKERFILE_SAPLING_BUILD

    with open(f"{ARTIFACTS_DIR}/Dockerfile_sapling_build", mode='w') as temp_file:
        temp_file.write(dockerfile_sapling_build_contents)
        temp_file.flush()

    # Arm64 build
    if CPU_ARCH == "arm64":
        subprocess.check_call(f"docker build -t sapling_{CPU_ARCH}:latest -f {ARTIFACTS_DIR}/Dockerfile_sapling_build {SAPLING_DIR}", shell=True)
        subprocess.check_call(f"docker create --name temp-container sapling_{CPU_ARCH}:latest", shell=True)
        subprocess.check_call(f"docker cp temp-container:/tmp/sapling.deb {ARTIFACTS_DIR}/sapling_{CPU_ARCH}.deb", shell=True)
        subprocess.check_call(f"docker rm temp-container", shell=True)
    else:
        raise Exception(f"CPU_ARCH must be arm64. Have {CPU_ARCH}")

# # unused for now
# def multi_arch_build():
#     #############################
#     # Configure the builder
#     builder_exists = False
#     try:
#         subprocess.check_call("docker buildx inspect sapling_multiarchbuilder", shell=True)
#         builder_exists = True
#     except Exception:
#         builder_exists = False

#     # enable QEMU for arm64 / amd64 emulataion
#     subprocess.check_call("docker run --privileged --rm tonistiigi/binfmt --install all", shell=True)
#     if not builder_exists:
#         subprocess.check_call("docker buildx create --name sapling_multiarchbuilder --driver docker-container --use", shell=True)
#         subprocess.check_call("docker buildx inspect sapling_multiarchbuilder --bootstrap", shell=True)
    
#     # Multi arch build -- buildx
#     subprocess.check_call(f"docker login", shell=True)
#     subprocess.check_call(f"docker buildx build --builder sapling_multiarchbuilder --platform linux/arm64 -t nhandyal/sapling:latest-arm64 -f {ARTIFACTS_DIR}/Dockerfile_sapling_build {SAPLING_DIR}", shell=True)
#     subprocess.check_call(f"docker buildx build --builder sapling_multiarchbuilder --platform linux/amd64 -t nhandyal/sapling:latest-amd64 -f {ARTIFACTS_DIR}/Dockerfile_sapling_build {SAPLING_DIR}", shell=True)
#     subprocess.check_call(f"docker push nhandyal/nhandyal-images:sapling_{CPU_ARCH}", shell=True)


if __name__ == "__main__":
     build()
