#!/bin/bash

clear
source .venv/bin/activate

set -e

BLACK_PATH="build/tools/black"
PYLINT_PATH="build/tools/pylint"
PYTEST_PATH="build/tools/pytest"

mkdir -p "$BLACK_PATH" "$PYLINT_PATH" "$PYTEST_PATH"

# Check if '-v' is passed as an argument
VERBOSE=""
for arg in "$@"
do
    if [ "$arg" = "-v" ]; then
        VERBOSE="--verbose"
    fi
done

echo " "
echo "--------- BLACK ---------------------------"
echo " "
if ! black src tests --config pyproject.toml $VERBOSE 2>&1 | tee "$BLACK_PATH/black_output.txt"; then
    echo "Black found format issues or encountered an error."
    exit 1
fi

echo " "
echo "--------- PYLINT ---------------------------"
echo " "
if ! pylint --rcfile pyproject.toml src tests $VERBOSE 2>&1 | tee "$PYLINT_PATH/pylint_output.txt"; then
    echo "Pylint encountered issues or errors."
    exit 1
fi

echo " "
echo "--------- PYTEST /W COVERAGE ---------------------------"
echo " "
if ! pytest $VERBOSE 2>&1 | tee "$PYTEST_PATH/pytest_output.txt"; then
    echo "Pytest encountered errors."
    exit 1
fi

deactivate
