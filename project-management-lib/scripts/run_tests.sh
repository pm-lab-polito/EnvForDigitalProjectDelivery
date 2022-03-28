#!/bin/bash
set -xe

SCRIPT_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)

cd $SCRIPT_DIR && echo "Inside Script directory"

bash setup.sh || exit 1

cd ..

source venv/bin/activate

pytest --cov-report=term-missing --cov=src --disable-network -xsv --cov-fail-under=90

echo "writing coverage..."

coverage json

deactivate
