#!/usr/bin/env bash

set -e

SOURCE=${BASH_SOURCE[0]}
while [ -L "$SOURCE" ]; do
  DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
  SOURCE=$(readlink "$SOURCE")
  [[ $SOURCE != /* ]] && SOURCE=$DIR/$SOURCE
done
DIR=$( cd -P "$( dirname "$SOURCE" )" >/dev/null 2>&1 && pwd )
ROOT="$(realpath $DIR/../)"

echo "Running pre-commit checks"

echo ""
echo "Running code formatters..."
fmt
echo "Done"

echo ""
echo "Running typecheckers..."
pyright
echo "Done"

echo ""
echo "Running linters..."
lint
echo "Done"

echo ""
echo "Running code complexity checks..."
rdx --no-color --min-rank C
echo "Done"

echo ""
echo "Running tests..."
t
echo "Done"

echo ""
echo "pre-commit checks: Done"
