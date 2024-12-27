#!/bin/bash

# List of packages to check
packages=("numpy" "pandas" "scipy")

# Loop through each package and check if it's installed
for package in "${packages[@]}"; do
    python3 -c "import $package" &>/dev/null
    if [ $? -eq 0 ]; then
        echo "$package is installed."
    else
        echo "$package is NOT installed."
        
    fi
done
