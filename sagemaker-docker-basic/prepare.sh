#!/usr/bin/env bash

# Fail on errors
set -o errexit

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

chmod +x ${__dir}/entrypoint_train.py

rm -rf tmp
# PRIVATE DEPENDENCIES
echo "Cloning PRIVATE-REPO..."
git clone git@github.com:COMPANY/PRIVATE-REPO.git tmp/PRIVATE-REPO