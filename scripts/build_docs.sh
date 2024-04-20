#!/bin/bash

SPHINX_PATH="build/docs/sphinx"

mkdir -p "$SPHINX_PATH"

source .venv/bin/activate

cd docs
make clean
make html 2>&1 | tee "../$SPHINX_PATH/sphinx_output.txt"
cd ..

open $SPHINX_PATH/html/index.html

deactivate
