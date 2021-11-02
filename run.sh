#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset

set -o xtrace

./knocker.py 2>&1 | tee -a run.log
