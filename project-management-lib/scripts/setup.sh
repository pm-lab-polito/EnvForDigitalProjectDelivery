#!/bin/bash
set -xe

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

echo "$SCRIPT_DIR"

cd $SCRIPT_DIR

cd ..

[[ ! -d venv ]] && python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

pre-commit install
