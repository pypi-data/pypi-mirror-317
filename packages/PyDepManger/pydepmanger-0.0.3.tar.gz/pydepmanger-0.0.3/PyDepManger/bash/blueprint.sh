#!/bin/bash

# Check if the language is passed as an argument
if [ -z "$1" ]; then
    echo "Please provide a programming language (py, scala, java, c)."
    exit 1
fi

# Function to check for each language
check_language() {
    local lang=$1

    # Handle Python
    if [[ "$lang" == "py" ]]; then
        if command -v python3 &> /dev/null; then
            echo "Python 3 is installed."
            python3 --version
            echo "Python executable path: $(which python3)"
            echo "To change the PATH, add the directory above to your PATH environment variable."
        elif command -v python &> /dev/null; then
            echo "Python 2 is installed."
            python --version
            echo "Python executable path: $(which python)"
            echo "To change the PATH, add the directory above to your PATH environment variable."
        else
            echo "Python is not installed."
        fi

    # Handle Scala
    elif [[ "$lang" == "scala" ]]; then
        if command -v scala &> /dev/null; then
            echo "Scala is installed."
            scala -version
            echo "Scala executable path: $(which scala)"
            echo "To change the PATH, add the directory above to your PATH environment variable."
        else
            echo "Scala is not installed."
        fi

    # Handle Java
    elif [[ "$lang" == "java" ]]; then
        if command -v java &> /dev/null; then
            echo "Java is installed."
            java -version 2>&1 | head -n 1  # Capture the first line of java version (since it's printed to stderr)
            echo "Java executable path: $(which java)"
            echo "To change the PATH, add the directory above to your PATH environment variable."
        else
            echo "Java is not installed."
        fi

    # Handle C (Checking for GCC compiler)
    elif [[ "$lang" == "c" ]]; then
        if command -v gcc &> /dev/null; then
            echo "GCC (C Compiler) is installed."
            gcc --version
            echo "GCC executable path: $(which gcc)"
            echo "To change the PATH, add the directory above to your PATH environment variable."
        else
            echo "GCC (C Compiler) is not installed."
        fi

    else
        echo "Unsupported language. Please use py, scala, java, or c."
    fi
}

# Call the function with the argument passed
check_language "$1"
