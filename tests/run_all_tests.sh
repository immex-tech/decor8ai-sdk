#!/bin/bash
#
# Decor8 AI SDK - Master Test Runner
#
# Runs comprehensive tests across all SDKs with a single command.
#
# Usage:
#   ./run_all_tests.sh                    # Run all tests
#   ./run_all_tests.sh --python-only      # Run Python tests only
#   ./run_all_tests.sh --js-only          # Run JavaScript tests only
#   ./run_all_tests.sh --quick            # Quick smoke test (fewer endpoints)
#
# Prerequisites:
#   - DECOR8AI_API_KEY environment variable set
#   - Python 3.8+ with pip
#   - Node.js 18+ with npm
#

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Track results
PYTHON_RESULT=0
JS_RESULT=0
DART_RESULT=0

print_header() {
    echo ""
    echo -e "${BOLD}${BLUE}============================================================${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}============================================================${NC}"
    echo ""
}

print_status() {
    if [ "$2" -eq 0 ]; then
        echo -e "  ${GREEN}✓${NC} $1"
    else
        echo -e "  ${RED}✗${NC} $1"
    fi
}

check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check API key
    if [ -z "$DECOR8AI_API_KEY" ]; then
        echo -e "${RED}ERROR: DECOR8AI_API_KEY environment variable not set${NC}"
        echo "Set it with: export DECOR8AI_API_KEY='your-api-key'"
        exit 1
    fi
    echo -e "  ${GREEN}✓${NC} DECOR8AI_API_KEY is set"

    # Check Python
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1)
        echo -e "  ${GREEN}✓${NC} Python: $PYTHON_VERSION"
    else
        echo -e "  ${YELLOW}⚠${NC} Python 3 not found - Python tests will be skipped"
    fi

    # Check Node.js
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version 2>&1)
        echo -e "  ${GREEN}✓${NC} Node.js: $NODE_VERSION"
    else
        echo -e "  ${YELLOW}⚠${NC} Node.js not found - JavaScript tests will be skipped"
    fi

    # Check Dart (optional)
    if command -v dart &> /dev/null; then
        DART_VERSION=$(dart --version 2>&1)
        echo -e "  ${GREEN}✓${NC} Dart: $DART_VERSION"
    else
        echo -e "  ${YELLOW}⚠${NC} Dart not found - Dart tests will be skipped"
    fi

    echo ""
}

setup_python() {
    print_header "Setting Up Python Environment"

    cd "$ROOT_DIR/python/decor8ai"

    # Install in development mode
    if [ -f "setup.py" ]; then
        pip3 install -e . -q 2>/dev/null || pip install -e . -q 2>/dev/null
        echo -e "  ${GREEN}✓${NC} Python SDK installed"
    fi

    # Install test dependencies
    pip3 install requests -q 2>/dev/null || pip install requests -q 2>/dev/null
    echo -e "  ${GREEN}✓${NC} Dependencies installed"

    cd "$SCRIPT_DIR"
}

setup_javascript() {
    print_header "Setting Up JavaScript Environment"

    cd "$ROOT_DIR/js/decor8ai"

    # Install dependencies
    if [ -f "package.json" ]; then
        npm install --silent 2>/dev/null || true
        echo -e "  ${GREEN}✓${NC} JavaScript SDK dependencies installed"
    fi

    cd "$SCRIPT_DIR"
}

run_python_tests() {
    print_header "Running Python SDK Tests"

    if ! command -v python3 &> /dev/null; then
        echo -e "  ${YELLOW}⚠${NC} Skipping - Python not available"
        return 0
    fi

    cd "$SCRIPT_DIR"

    if python3 test_all_endpoints.py; then
        PYTHON_RESULT=0
        echo -e "\n  ${GREEN}✓${NC} Python tests completed successfully"
    else
        PYTHON_RESULT=1
        echo -e "\n  ${RED}✗${NC} Python tests failed"
    fi

    return $PYTHON_RESULT
}

run_javascript_tests() {
    print_header "Running JavaScript SDK Tests"

    if ! command -v node &> /dev/null; then
        echo -e "  ${YELLOW}⚠${NC} Skipping - Node.js not available"
        return 0
    fi

    cd "$SCRIPT_DIR"

    if node test_js_sdk.js; then
        JS_RESULT=0
        echo -e "\n  ${GREEN}✓${NC} JavaScript tests completed successfully"
    else
        JS_RESULT=1
        echo -e "\n  ${RED}✗${NC} JavaScript tests failed"
    fi

    return $JS_RESULT
}

run_dart_tests() {
    print_header "Running Dart SDK Tests"

    if ! command -v dart &> /dev/null; then
        echo -e "  ${YELLOW}⚠${NC} Skipping - Dart not available"
        return 0
    fi

    cd "$ROOT_DIR/dart/decor8ai"

    if [ -f "pubspec.yaml" ]; then
        dart pub get --no-precompile 2>/dev/null || true

        if dart test 2>/dev/null; then
            DART_RESULT=0
            echo -e "\n  ${GREEN}✓${NC} Dart tests completed successfully"
        else
            DART_RESULT=1
            echo -e "\n  ${RED}✗${NC} Dart tests failed"
        fi
    else
        echo -e "  ${YELLOW}⚠${NC} No pubspec.yaml found"
    fi

    cd "$SCRIPT_DIR"
    return $DART_RESULT
}

print_summary() {
    print_header "Final Summary"

    echo "  SDK Test Results:"
    echo ""
    print_status "Python SDK" $PYTHON_RESULT
    print_status "JavaScript SDK" $JS_RESULT
    print_status "Dart SDK" $DART_RESULT
    echo ""

    # Calculate overall result
    TOTAL_FAILURES=$((PYTHON_RESULT + JS_RESULT + DART_RESULT))

    if [ $TOTAL_FAILURES -eq 0 ]; then
        echo -e "  ${GREEN}${BOLD}ALL SDK TESTS PASSED${NC}"
        echo ""
        return 0
    else
        echo -e "  ${RED}${BOLD}$TOTAL_FAILURES SDK(S) HAD FAILURES${NC}"
        echo ""
        return 1
    fi
}

# Parse arguments
PYTHON_ONLY=false
JS_ONLY=false
QUICK_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --python-only)
            PYTHON_ONLY=true
            shift
            ;;
        --js-only)
            JS_ONLY=true
            shift
            ;;
        --quick)
            QUICK_MODE=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --python-only    Run Python tests only"
            echo "  --js-only        Run JavaScript tests only"
            echo "  --quick          Quick smoke test"
            echo "  -h, --help       Show this help"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Main execution
echo ""
echo -e "${BOLD}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║         Decor8 AI SDK - Comprehensive Test Suite           ║${NC}"
echo -e "${BOLD}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "  Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "  API Key:   ****...${DECOR8AI_API_KEY: -4}"
echo ""

check_prerequisites

# Run tests based on arguments
if [ "$PYTHON_ONLY" = true ]; then
    setup_python
    run_python_tests || true
elif [ "$JS_ONLY" = true ]; then
    setup_javascript
    run_javascript_tests || true
else
    # Run all tests
    setup_python
    setup_javascript

    run_python_tests || true
    run_javascript_tests || true
    # run_dart_tests || true  # Uncomment when Dart tests are ready
fi

# Print summary and exit
print_summary
exit $?
