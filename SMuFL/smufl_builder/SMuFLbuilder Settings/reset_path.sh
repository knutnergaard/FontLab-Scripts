#! /bin/bash

# Settings path replacer for SMuFLbuilder.
# =============================================================================

# This shell script replaces the path of the user variable in smuflbuilder/
# filepaths.py with path of the .ini file sharing this scripts directory.

# Kepping a copy of this script in the same directory as any versions of
#smuflbuilder.ini, will make switching between different settings files easier.

parent=$(dirname -- "$0")
filepath=$(find "$parent" -type f -name "*.ini")
paths="$HOME/Library/Application Support/FontLab/Studio 5/Macros/System/\
Modules/smuflbuilder/filepaths.py"

if [[ $filepath ]]; then
    sed -i '' "s|user = '.*'|user = '$filepath'|g" "$paths"
    echo "Path reset to: $filepath"
else
    echo "No settings file found!"
fi
