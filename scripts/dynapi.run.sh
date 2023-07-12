#!/usr/bin/bash
THIS=$(dirname "$(realpath "$0")")
cd "$THIS" || exit 1
python3 -B -O __main__.py "$@"
