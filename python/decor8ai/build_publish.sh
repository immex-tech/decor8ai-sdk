#!/bin/bash

# Get the current version from pyproject.toml
get_current_version() {
    grep -E '^version' pyproject.toml | sed 's/version = "//' | sed 's/"//'
}

# Increment the version number
increment_version() {
    echo "$1" | awk -F. '{$NF = $NF + 1;} 1' OFS=.
}

# Update version in pyproject.toml
update_version() {
    sed -i "" "s/^version = .*/version = \"$1\"/" pyproject.toml
}

# Check if version is passed as an argument
if [ "$#" -eq 1 ]; then
    NEW_VERSION=$1
else
    CURRENT_VERSION=$(get_current_version)
    NEW_VERSION=$(increment_version $CURRENT_VERSION)
fi

# Update the version in pyproject.toml
update_version $NEW_VERSION

# Remove the existing dist directory
rm -rf dist

# Build the package
poetry build

# Publish the package
poetry publish

echo "Package built and published as version $NEW_VERSION"
