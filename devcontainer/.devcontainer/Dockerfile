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
