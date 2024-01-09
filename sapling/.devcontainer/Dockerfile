FROM ubuntu:20.04

RUN apt-get update -y && apt-get install -y \
    ca-certificates curl git gnupg sudo vim wget locales

RUN apt-get update && apt-get install -y curl && \
    ARCH=$(dpkg --print-architecture) && \
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

# verify sapling installed correctlty
RUN sl

CMD ["tail", "-f", "/dev/null"]
