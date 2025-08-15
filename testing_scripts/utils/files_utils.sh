#!/bin/bash
set -e

find_file() {
    local folder_name="$1"
    local search_term="$2"

    if [ -z "$search_term" ]; then
        echo "❌ Usage: find_adjacent_file <mot_à_chercher>"
        return 1
    fi

    local base_dir
    base_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    local inspected_dir="${base_dir}/../../${folder_name}"

    local found_file
    found_file=$(find "$inspected_dir" -maxdepth 1 -type f -name "*${search_term}*" | head -n 1)

    if [ -z "$found_file" ]; then
        echo "❌ No file containing : $search_term"
        return 1
    fi

    found_file="$(basename "$found_file")"

    echo "$found_file"
}

