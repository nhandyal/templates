FROM ubuntu:20.04

ARG GROUP_NAME=staff
ARG GROUP_ID=20
ARG USER_NAME=apollo
ARG USER_ID=501

ARG NODE_MAJOR=20

# https://serverfault.com/a/1016972 to ensure installing tzdata does not
# result in a prompt that hangs forever.
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

#######
# Install system packages 1
RUN apt-get update -y && apt-get install -y \
    ca-certificates curl git gnupg

#######
# Get GH ready to install
RUN type -p curl >/dev/null || (apt update && apt install curl -y) && \
    curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list > /dev/null

#######
# Get Node ready to install
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | tee /etc/apt/sources.list.d/nodesource.list

#######
# Install system packages 2
RUN apt-get update -y && apt-get install -y \
    coreutils cython3 dpkg-dev gcc g++ gh libffi-dev libssl-dev locales make nodejs openssh-client pkg-config procps python3.8 python3.8-dev python3.8-distutils sudo vim wget && \
    rm -rf /var/lib/apt/lists/*

#######
# Install sapling
RUN ARCH=$(dpkg --print-architecture) && \
    case "$ARCH" in \
    amd64) URL="https://github.com/facebook/sapling/releases/download/0.2.20231113-145254%2B995db0d6/sapling_0.2.20231113-145254%2B995db0d6_amd64.Ubuntu20.04.deb" ;; \
    arm64) URL="https://storage.googleapis.com/regulus-public/sapling_arm64.deb" ;; \
    *) echo "Unsupported architecture: $ARCH" && exit 1 ;; \
    esac && \
    curl -L -o sapling.deb "$URL" && \
    dpkg -i sapling.deb && \
    rm sapling.deb && \
    curl -L -o '/etc/default/locale' 'https://storage.googleapis.com/regulus-public/default_locale' && \
    curl -L -o '/etc/locale.gen' 'https://storage.googleapis.com/regulus-public/locale.gen' && \
    locale-gen

#######
# Install conda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH=/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN	/bin/sh -c set -x && \
	apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends bzip2 libglib2.0-0 libsm6 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxinerama1 libxrandr2 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ARCH=$(dpkg --print-architecture) && \
    case "$ARCH" in \
    amd64) ANACONDA_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh"; SHA256SUM="6c8a4abb36fbb711dc055b7049a23bbfd61d356de9468b41c5140f8a11abd851" ;; \
    arm64) ANACONDA_URL="https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-aarch64.sh"; SHA256SUM="69ee26361c1ec974199bce5c0369e3e9a71541de7979d2b9cfa4af556d1ae0ea" ;; \
    *) echo "Unsupported architecture: $ARCH" && exit 1 ;; \
    esac && \
    wget "${ANACONDA_URL}" -O anaconda.sh && \
    echo "${SHA256SUM} anaconda.sh" > shasum && \
    sha256sum --check --status shasum && \
    /bin/bash anaconda.sh -b -p /opt/conda && \
    rm anaconda.sh shasum && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

# Create a new group and user with the specified IDs and names
RUN if ! getent group $GROUP_NAME; then \
    groupadd -g $GROUP_ID $GROUP_NAME; \
    fi

RUN if ! getent passwd $USER_NAME; then \
    useradd -ms /bin/bash -g $GROUP_NAME -u $USER_ID $USER_NAME; \
    fi

# Add user to sudoers without password
RUN echo "$USER_NAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Clean up to reduce the size of the Docker image.
RUN rm -rf /tmp/repo

###########################
## USER CONFIG ##

USER $USER_NAME

RUN mkdir -p /home/$USER_NAME/.config/sapling

COPY configs/bashrc /home/$USER_NAME/.bashrc
COPY configs/bash_profile /home/$USER_NAME/.bash_profile
COPY configs/gitconfig /home/$USER_NAME/.gitconfig
COPY configs/slconfig /home/$USER_NAME/.config/sapling/sapling.conf

RUN sudo chown -R $USER_NAME:$GROUP_NAME /home/$USER_NAME

###########################
## END USER CONFIG ##

USER $USER_NAME
CMD ["tail", "-f", "/dev/null"]
