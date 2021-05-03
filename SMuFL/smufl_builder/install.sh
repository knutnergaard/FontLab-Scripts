#! /bin/bash

# Installer script for SMuFLbuilder on Mac.

# This script will move all package folders to the correct directories.
# Except for the module folder (smuflbuilder/), files will be copied into any
# preexisting folders.

# Function to set .ini filepath (set_path.sh) is run after installation.

# User will be prompted before anything is overwritten.

# Folder names and their destinations:

# SMuFL/
#  --> ~/Library/Application Support/FontLab/Studio 5/Macros/
# smuflbuilder/
#  --> ~/Library/Application Support/FontLab/Studio 5/Macros/System/Modules/
# SMuFLbuilder Settings/
#  --> ~/Documents


function inform() {
    # Ask for permission to overwrite if file exists. Act accordingly.

    local filder=$1

    while true; do
        read -p "$filder already exists. Do you want to overwrite it? Y/N"\
        answer
        case "$answer" in
            [yY] | [yY][eE][sS])
                break
                ;;
            [nN] | [nN][oO])
                return 1
                ;;
            *)
                echo "Please enter y/yes or n/no!"
        esac
    done
}

function install() {
    # Moves directory if none-existent.
    # Calls inform for permission to overwrite
    # and informs of replacement otherwise.

    local path=$1
    local parent=$2
    local file=$3

    # Move dir if non-existent.
    if ! [[ -d "$path/$parent/" ]]; then
        echo "Moving $parent/ ..."
        mv "$PWD/$parent/" "$path/$parent/"

    # Replace module dir if permission granted and inform.
    elif [[ "$parent" == $module_parent ]]; then
        inform "$parent"
        if [[ "${?}" -eq 0 ]]; then
            echo "Replacing $parent/ ..."
            rm -r "$path/$parent/"
            mv "$PWD/$parent/" "$path/$parent/"
        else
            echo "Skipping $parent"
        fi

    # Replace file if permission granted.
    elif [[ -f "$path/$parent/$file" ]]; then
        inform "$file"
        if [[ "${?}" -eq 0 ]]; then
            echo "Replacing $file ..."
            echo "$PWD/$parent/$file" "$path/$parent/"
        else
            echo "Skipping $file"
        fi

    # Move file if non-existent.
    else
        echo "Moving $file ..."
        echo "$PWD/$parent/$file" "$path/$parent/"
    fi
}

function set_path(){
# Copy of code in reset_path.sh to reset filepath to smuflbuilder.ini.

    local parent=$(dirname -- "$0")
    local filepath=$(find "$parent" -type f -name "*.ini")
    local paths="$HOME/Library/Application Support/FontLab/Studio 5/Macros/\
    System/Modules/smuflbuilder/filepaths.py"

    if [[ $filepath ]]; then
        sed -i '' "s|user = '.*'|user = '$filepath'|g" "$paths"
        echo "Setting smuflbuilder.ini filepath ..."
    fi
}


macro_path="$HOME/Library/Application Support/FontLab/Studio 5/Macros"
module_path="$HOME/Library/Application Support/FontLab/Studio 5/Macros/System/Modules"
config_path="$HOME/Documents"
macro_parent="SMuFL"
macro="smuflbuilder.py"
module_parent="smuflbuilder"
config_parent="SMuFLbuilder Settings"
config="smuflbuilder.ini"
config_script="replace_settings.sh"

install "$macro_path" "$macro_parent" "$macro"
install "$module_path" "$module_parent" ""
install "$config_path" "$config_parent" "$config"
install "$config_path" "$config_parent" "$config_script"

set_path

echo "All done!"
