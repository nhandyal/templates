FROM nhandyal/base:latest

ARG USER_NAME=nrh

#######
# Install conda
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
USER root
RUN	/bin/sh -c set -x && \
	apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends bzip2 libglib2.0-0 libsm6 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 libxinerama1 libxrandr2 libxrender1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    ARCH=$(dpkg --print-architecture) && \
    case "$ARCH" in \
    amd64) MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-py38_23.11.0-2-Linux-x86_64.sh"; SHA256SUM="cb908ddbd603d789d94076ea4dd3f8517b15866719e007725dca778a8dfab823" ;; \
    arm64) MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-py38_23.11.0-2-Linux-aarch64.sh"; SHA256SUM="6e439ae5373d35b78a3f45775fa69f0afddd0c0a9e5e545cd2f75f913a6d143b" ;; \
    *) echo "Unsupported architecture: $ARCH" && exit 1 ;; \
    esac && \
    wget "${MINICONDA_URL}" -O miniconda.sh && \
    echo "${SHA256SUM} miniconda.sh" |  tee -a shasum && \
    sha256sum --check --status shasum && \
    chmod +x miniconda.sh && \
    /bin/bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh shasum && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    find /opt/conda/ -follow -type f -name '*.a' -delete && \
    find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
    /opt/conda/bin/conda clean -afy

USER $USER_NAME
RUN /bin/bash -c "source /opt/conda/bin/activate && \
    conda init --all && \
    conda activate base"
