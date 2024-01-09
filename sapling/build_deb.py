#!/usr/bin/env python3

import os
import subprocess
import tempfile

CPU_ARCH_REMAP = {
    "x86_64": "amd64",
    "amd64": "amd64",
    "aarch64": "arm64",
    "arm64": "arm64",
}

CPU_ARCH = CPU_ARCH_REMAP[os.uname().machine]

# Targeting Ubuntu 20.04
PY_VERSION=38
GIT_DEB_DEP="git (>= 1:2.25.1)"


def main():
    with open("../../SAPLING_VERSION", "r") as f:
        sapling_version = f.read().strip()

    subprocess.check_call("DESTDIR=install make PREFIX=/usr install-oss", shell=True)
    
    # For simplicity, we currently use `dpkg-deb --build`, though we should
    # ultimately migrate to dpkg-buildpackage. Because we are going to mess with
    # the contents of the install folder, we create a copy to work with instead.
    temp_dir = tempfile.TemporaryDirectory()
    subprocess.check_call(f"cp --recursive install {temp_dir.name}", shell=True)
    subprocess.check_call(f"mkdir -p {temp_dir.name}/install/debian", shell=True)
    subprocess.check_call(f"cp packaging/debian/control {temp_dir.name}/install/debian/control", shell=True)

    # dpkg-shlibdeps requires the file `debian/control` to exist in the folder in which it is run.
    deb_deps = subprocess.check_output(f"dpkg-shlibdeps -O -e usr/bin/*", shell=True, cwd=f"{temp_dir.name}/install").decode("utf-8").strip()
    
    # dpkg-shlibdeps does not know about the runtime dependency on Git, so it must be added explicitly.
    deb_deps += f", {GIT_DEB_DEP}"
    
    # In contrast to dpkg-shlibdeps, dpkg-deb requires the file to be named
    # `DEBIAN/control`, so we rename the directory and proceed.
    subprocess.check_call(f"mv {temp_dir.name}/install/debian {temp_dir.name}/install/DEBIAN", shell=True)
    
    with open(f"{temp_dir.name}/install/DEBIAN/control", "r") as f:
        control = f.read()
    
    control += deb_deps.replace('shlibs:Depends=', 'Depends: ') + "\n"
    control = control.replace("Version: %VERSION%", f"Version: {sapling_version}")
    control = control.replace("Architecture: amd64", f"Architecture: {CPU_ARCH}")

    print(control)
    print(f"{temp_dir.name}/install/DEBIAN/control")

    with open(f"{temp_dir.name}/install/DEBIAN/control", "w") as f:
        f.write(control)
        f.flush()

    subprocess.check_call("dpkg-deb --build --root-owner-group install", cwd=temp_dir.name, shell=True)

    subprocess.check_call(f"cp {temp_dir.name}/install.deb .", shell=True)
    subprocess.check_call(f"dpkg-name install.deb", shell=True)

if __name__ == "__main__":
    main()
