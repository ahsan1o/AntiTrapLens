#!/usr/bin/env python3
"""
Quick demo script for AntiTrapLens
Run this to see the tool in action with sample websites
"""

import subprocess
import sys
import os

def run_demo():
    """Run a quick demo of AntiTrapLens"""

    print("🔍 AntiTrapLens Demo")
    print("=" * 50)

    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ Error: Please run this script from the AntiTrapLens root directory")
        sys.exit(1)

    # Check if virtual environment is activated
    if "venv" not in sys.executable:
        print("⚠️  Warning: Virtual environment not detected")
        print("   Consider running: source venv/bin/activate")
        print()

    print("🚀 Running demo scan on example.com...")
    print()

    try:
        # Run a simple scan
        result = subprocess.run([
            sys.executable, "main.py",
            "https://example.com",
            "--verbose",
            "--report-format", "console"
        ], capture_output=True, text=True, timeout=60)

        print("📊 Demo Results:")
        print("-" * 30)
        print(result.stdout)

        if result.stderr:
            print("⚠️  Warnings/Errors:")
            print(result.stderr)

        print("\n✅ Demo completed successfully!")
        print("\n💡 Try these next:")
        print("   python main.py https://example.com --depth 2 --report-format html")
        print("   python main.py https://httpbin.org --verbose")

    except subprocess.TimeoutExpired:
        print("⏰ Demo timed out - the scan might be taking longer than expected")
    except FileNotFoundError:
        print("❌ Error: main.py not found or Python not available")
    except Exception as e:
        print(f"❌ Error running demo: {e}")

if __name__ == "__main__":
    run_demo()
