#!/usr/bin/env bash

set -e

SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )


if [ -d "$DIR/../generated" ]; then
    rm -rf "$DIR/../generated"
fi
mkdir -p "$DIR/../generated"


# Check if Python 3 is available
if command -v python3 &> /dev/null
then
    echo "Using Python 3"
    python3 "$DIR/generate_vcs_configs.py"
else
    echo "Using Python"
    python "$DIR/generate_vcs_configs.py"
fi