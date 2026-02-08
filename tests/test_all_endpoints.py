#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Decor8 AI SDK

This script tests ALL API endpoints across the SDK to ensure everything works.
Run with: python test_all_endpoints.py

Requires:
    - DECOR8AI_API_KEY environment variable set
    - requests package (pip install requests)

Output:
    - Console output with pass/fail for each endpoint
    - JSON report at tests/results/test_report.json
    - Exit code 0 if all pass, 1 if any fail
"""

import os
import sys
import json
import time
import traceback
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "python" / "decor8ai"))

# Test configuration - using exact images from server tests
CONFIG = {
    "test_images": {
        "room": "https://prod-files.decor8.ai/test-images/sdk_test_image.png",
        "remove_objects": "https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_bedroom_1.jpg",
        "wall_color": "https://prod-files.decor8.ai/test-images/sdk_test_remove_objects_bedroom_1.jpg",
        "kitchen_cabinets": "https://prod-files.decor8.ai/test-images/sdk_test_change_kitchen_cabinets_color_1.jpg",
        "kitchen_remodel": "https://prod-files.decor8.ai/test-images/sdk_test_remodel_kitchen.png",
        "bathroom_remodel": "https://prod-files.decor8.ai/test-images/sdk_test_remodel_bathroom.png",
        "landscaping": "https://prod-files.decor8.ai/test-images/sdk_test_landcape_designs_front_yard.jpeg",
        "sky_replacement": "https://prod-files.decor8.ai/test-images/sdk_replace_sky_test_image.png",
        "sketch": "https://prod-files.decor8.ai/test-images/sdk_sketch_to_3d_render.png",
    },
    "test_params": {
        "room_type": "livingroom",
        "design_style": "modern",
        "wall_color": "#FF5733",
        "cabinet_color": "#8B4513",
        "sky_type": "day",
        "yard_type": "front yard",
        "garden_style": "california style garden",
    },
}


class Colors:
    """ANSI color codes for terminal output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text.center(60)}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_result(name, success, duration, error=None):
    status = f"{Colors.GREEN}PASS{Colors.END}" if success else f"{Colors.RED}FAIL{Colors.END}"
    print(f"  [{status}] {name} ({duration:.2f}s)")
    if error:
        print(f"        {Colors.RED}Error: {error}{Colors.END}")


def test_endpoint(name, func, *args, **kwargs):
    """Test a single endpoint and return result."""
    start = time.time()
    try:
        result = func(*args, **kwargs)
        duration = time.time() - start

        # Check for API errors in response
        if isinstance(result, dict):
            if result.get('error'):
                return {
                    "name": name,
                    "success": False,
                    "duration": duration,
                    "error": result.get('error') + ': ' + result.get('message', ''),
                }
            # Check for images in response (most endpoints return images)
            if 'info' in result and 'images' in result['info']:
                if len(result['info']['images']) == 0:
                    return {
                        "name": name,
                        "success": False,
                        "duration": duration,
                        "error": "No images returned",
                    }

        return {
            "name": name,
            "success": True,
            "duration": duration,
            "error": None,
        }
    except Exception as e:
        duration = time.time() - start
        return {
            "name": name,
            "success": False,
            "duration": duration,
            "error": str(e),
        }


def run_python_sdk_tests():
    """Run all Python SDK tests."""
    print_header("Python SDK Tests")

    results = []

    try:
        from decor8ai import (
            Decor8AI,
            generate_designs_for_room,
            generate_inspirational_designs,
            prime_walls_for_room,
            replace_sky_behind_house,
            remove_objects_from_room,
            change_wall_color,
            change_kitchen_cabinets_color,
            remodel_kitchen,
            remodel_bathroom,
            generate_landscaping_designs,
            sketch_to_3d_render,
        )
    except ImportError as e:
        print(f"{Colors.RED}Failed to import Python SDK: {e}{Colors.END}")
        return [{"name": "Python SDK Import", "success": False, "duration": 0, "error": str(e)}]

    # Test 1: Generate Designs for Room
    r = test_endpoint(
        "generate_designs_for_room",
        generate_designs_for_room,
        input_image_url=CONFIG["test_images"]["room"],
        room_type=CONFIG["test_params"]["room_type"],
        design_style=CONFIG["test_params"]["design_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 2: Generate Inspirational Designs
    r = test_endpoint(
        "generate_inspirational_designs",
        generate_inspirational_designs,
        room_type=CONFIG["test_params"]["room_type"],
        design_style=CONFIG["test_params"]["design_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 3: Prime Walls for Room
    r = test_endpoint(
        "prime_walls_for_room",
        prime_walls_for_room,
        input_image_url=CONFIG["test_images"]["room"],
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 4: Replace Sky Behind House
    r = test_endpoint(
        "replace_sky_behind_house",
        replace_sky_behind_house,
        input_image_url=CONFIG["test_images"]["sky_replacement"],
        sky_type=CONFIG["test_params"]["sky_type"],
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 5: Remove Objects from Room
    r = test_endpoint(
        "remove_objects_from_room",
        remove_objects_from_room,
        input_image_url=CONFIG["test_images"]["remove_objects"],
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 6: Change Wall Color
    r = test_endpoint(
        "change_wall_color",
        change_wall_color,
        input_image_url=CONFIG["test_images"]["wall_color"],
        wall_color_hex_code=CONFIG["test_params"]["wall_color"],
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 7: Change Kitchen Cabinets Color
    r = test_endpoint(
        "change_kitchen_cabinets_color",
        change_kitchen_cabinets_color,
        input_image_url=CONFIG["test_images"]["kitchen_cabinets"],
        cabinet_color_hex_code=CONFIG["test_params"]["cabinet_color"],
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 8: Remodel Kitchen
    r = test_endpoint(
        "remodel_kitchen",
        remodel_kitchen,
        input_image_url=CONFIG["test_images"]["kitchen_remodel"],
        design_style=CONFIG["test_params"]["design_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 9: Remodel Bathroom
    r = test_endpoint(
        "remodel_bathroom",
        remodel_bathroom,
        input_image_url=CONFIG["test_images"]["bathroom_remodel"],
        design_style=CONFIG["test_params"]["design_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 10: Generate Landscaping Designs
    r = test_endpoint(
        "generate_landscaping_designs",
        generate_landscaping_designs,
        input_image_url=CONFIG["test_images"]["landscaping"],
        yard_type=CONFIG["test_params"]["yard_type"],
        garden_style=CONFIG["test_params"]["garden_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    # Test 11: Sketch to 3D Render
    r = test_endpoint(
        "sketch_to_3d_render",
        sketch_to_3d_render,
        input_image_url=CONFIG["test_images"]["sketch"],
        design_style=CONFIG["test_params"]["design_style"],
        num_images=1,
    )
    results.append(r)
    print_result(r["name"], r["success"], r["duration"], r["error"])

    return results


def generate_report(results, output_dir):
    """Generate JSON and text reports."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    passed = sum(1 for r in results if r["success"])
    failed = sum(1 for r in results if not r["success"])
    total_time = sum(r["duration"] for r in results)

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "success_rate": f"{(passed/len(results)*100):.1f}%" if results else "0%",
            "total_duration": f"{total_time:.2f}s",
        },
        "results": results,
    }

    # Write JSON report
    with open(output_dir / "test_report.json", "w") as f:
        json.dump(report, f, indent=2)

    return report


def print_summary(report):
    """Print test summary."""
    print_header("Test Summary")

    summary = report["summary"]

    if summary["failed"] == 0:
        status_color = Colors.GREEN
        status_text = "ALL TESTS PASSED"
    else:
        status_color = Colors.RED
        status_text = f"{summary['failed']} TEST(S) FAILED"

    print(f"  Total Tests:    {summary['total']}")
    print(f"  Passed:         {Colors.GREEN}{summary['passed']}{Colors.END}")
    print(f"  Failed:         {Colors.RED}{summary['failed']}{Colors.END}")
    print(f"  Success Rate:   {summary['success_rate']}")
    print(f"  Total Duration: {summary['total_duration']}")
    print()
    print(f"  {status_color}{Colors.BOLD}{status_text}{Colors.END}")
    print()

    # List failed tests
    failed_tests = [r for r in report["results"] if not r["success"]]
    if failed_tests:
        print(f"  {Colors.RED}Failed Tests:{Colors.END}")
        for test in failed_tests:
            print(f"    - {test['name']}: {test['error']}")
        print()


def main():
    """Main test runner."""
    print(f"\n{Colors.BOLD}Decor8 AI SDK - Comprehensive Test Suite{Colors.END}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Check API key
    if not os.environ.get('DECOR8AI_API_KEY'):
        print(f"\n{Colors.RED}ERROR: DECOR8AI_API_KEY environment variable not set{Colors.END}")
        print("Set it with: export DECOR8AI_API_KEY='your-api-key'")
        sys.exit(1)

    print(f"API Key: {'*' * 20}...{os.environ['DECOR8AI_API_KEY'][-4:]}")

    all_results = []

    # Run Python SDK tests
    python_results = run_python_sdk_tests()
    all_results.extend(python_results)

    # Generate report
    output_dir = Path(__file__).parent / "results"
    report = generate_report(all_results, output_dir)

    # Print summary
    print_summary(report)

    print(f"  Report saved to: {output_dir / 'test_report.json'}")

    # Exit with appropriate code
    sys.exit(0 if report["summary"]["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
