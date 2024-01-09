# Sapling_build

# Overview
This repo contains scripts to build Sapling SCM from source and upload the pre-built bundle to Google Cloud. Sapling does not distribute linux arm binaries which are required for docker containers running on arm hosts (M* Macs).

# Files
- `build.py` - This script contains all the instructions to build sapling from source. It downloads the source repo, builds the binary in a container, and downloads the binary bundle to the host machine.
- `build_deb.pu` - A script that is inserted into the container that builds sapling. It is used to create the DEB package. The build_deb.sh file that comes with sapling doesn't complete succesfully. This script should not be run manually. It is inserted into the build container by build.py and the generated build docker file.
- `.devcontainer/Dockerfile` - Creates a dev environment with sapling installed. It is CPU arch aware.
- `sapling_init` -- This script converts a git repository into a sapling one. It replaces the .git directory with a .sl directory and deletes the .git directory.

## How to install in another container
Copy the commands in `Dockerfile_sapling` into the Dockerile that needs to install sapling

## Where to store the bundle
In Google Cloud -> Regulus project -> regulus_public bucket [link](https://console.cloud.google.com/storage/browser/regulus-public)

## Locales
Sometimes sapling can complain about locales not being installed
```
# To check if locales are installed
if ! locale -a | grep -qE '^(en_US |en_US.iso88591|en_US.iso885915|en_US.utf8)$'; then
    echo "en locales not installed"
fi

# If locales are not installed, run:
  sudo dpkg-reconfigure locales

All of the EN locales should be installed. These are typically
  157. en_US ISO-8859-1
  158. en_US.ISO-8859-15 ISO-8859-15
  159. en_US.UTF-8 UTF-8

Set the default to en_US.UTF-8
```
