#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PLUGIN_SLUG="decor8ai-virtual-staging"
MAIN_FILE="decor8ai-virtual-staging.php"
README_FILE="readme.txt"
CURRENT_DIR=$(pwd)
BUILD_DIR="$CURRENT_DIR/build"
DIST_DIR="$CURRENT_DIR/dist"

# Function to print status
print_status() {
    echo -e "${GREEN}➤ $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}✖ $1${NC}"
    exit 1
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Check if required files exist
if [ ! -f "$MAIN_FILE" ]; then
    print_error "Main plugin file $MAIN_FILE not found!"
fi

if [ ! -f "$README_FILE" ]; then
    print_error "README file $README_FILE not found!"
fi

# Get version from readme.txt
VERSION=$(grep "^Stable tag:" "$README_FILE" | awk -F' ' '{print $3}')
if [ -z "$VERSION" ]; then
    print_error "Could not find version in $README_FILE"
fi

# Create clean build directory
print_status "Creating build directory..."
rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR/$PLUGIN_SLUG"

# Create dist directory if it doesn't exist
mkdir -p "$DIST_DIR"

# Copy all required files to build directory
print_status "Copying files..."
cp -R includes templates assets "$BUILD_DIR/$PLUGIN_SLUG/"
cp $MAIN_FILE "$BUILD_DIR/$PLUGIN_SLUG/"
cp readme.txt "$BUILD_DIR/$PLUGIN_SLUG/"
cp LICENSE "$BUILD_DIR/$PLUGIN_SLUG/" 2>/dev/null || print_warning "No LICENSE file found"

# Remove unnecessary files
print_status "Cleaning up build directory..."
cd "$BUILD_DIR/$PLUGIN_SLUG"
find . -name '*.git*' -exec rm -rf {} +
find . -name '*.DS_Store' -exec rm -f {} +
find . -name 'node_modules' -exec rm -rf {} +
find . -name 'wp-test' -exec rm -rf {} +
find . -name 'tests' -exec rm -rf {} +
find . -name '*.map' -exec rm -f {} +
find . -name '*.log' -exec rm -f {} +
find . -name 'phpunit.xml*' -exec rm -f {} +
find . -name '.travis.yml' -exec rm -f {} +
find . -name '.env*' -exec rm -f {} +

# Optimize JavaScript files (if Node.js is available)
if command -v node &> /dev/null; then
    print_status "Optimizing JavaScript files..."
    if [ -d "assets/js" ]; then
        for file in assets/js/*.js; do
            if [ -f "$file" ] && [[ "$file" != *.min.js ]]; then
                if command -v uglifyjs &> /dev/null; then
                    uglifyjs "$file" -o "${file%.js}.min.js" -c -m
                    rm "$file"
                else
                    print_warning "uglify-js not found. Skipping JS optimization."
                fi
            fi
        done
    fi
fi

# Optimize CSS files (if Node.js is available)
if command -v node &> /dev/null; then
    print_status "Optimizing CSS files..."
    if [ -d "assets/css" ]; then
        for file in assets/css/*.css; do
            if [ -f "$file" ] && [[ "$file" != *.min.css ]]; then
                if command -v cleancss &> /dev/null; then
                    cleancss -o "${file%.css}.min.css" "$file"
                    rm "$file"
                else
                    print_warning "clean-css-cli not found. Skipping CSS optimization."
                fi
            fi
        done
    fi
fi

# Create zip file
print_status "Creating zip file..."
cd "$BUILD_DIR"
ZIP_FILE="$DIST_DIR/$PLUGIN_SLUG-$VERSION.zip"
zip -r "$ZIP_FILE" "$PLUGIN_SLUG" -x "*.DS_Store" -x "**/__MACOSX/**" -x "**/.git/**"

# Verify zip file
if [ -f "$ZIP_FILE" ]; then
    ZIP_SIZE=$(du -h "$ZIP_FILE" | cut -f1)
    print_status "Successfully created: $ZIP_FILE ($ZIP_SIZE)"
    print_status "Plugin version: $VERSION"
else
    print_error "Failed to create zip file!"
fi

# Cleanup
print_status "Cleaning up..."
rm -rf "$BUILD_DIR"

print_status "Build complete! 🎉"
echo -e "${GREEN}You can find the plugin zip at:${NC} $ZIP_FILE"

# Optional: Calculate checksums
if command -v md5sum &> /dev/null; then
    echo ""
    print_status "File checksums:"
    echo "MD5: $(md5sum "$ZIP_FILE" | awk '{print $1}')"
    echo "SHA1: $(sha1sum "$ZIP_FILE" | awk '{print $1}')"
    echo "SHA256: $(sha256sum "$ZIP_FILE" | awk '{print $1}')"
fi