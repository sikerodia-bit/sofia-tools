"""
sofia-tools installer
Copies tools from this library into your Sofia installation.

Usage:
  python install.py calculator
  python install.py url_reader
  python install.py bundle:utils
  python install.py bundle:caribbean
"""

import sys
import shutil
from pathlib import Path

SOFIA_PATH = Path("C:/xampp/htdocs/sofia")
TOOLS_PATH = Path("C:/xampp/htdocs/sofia-tools/tools")

BUNDLES = {
    "utils": [
        "utils/calculator.py",
        "utils/datetime_tool.py",
        "utils/web_search.py",
        "utils/memory_tool.py",
        "utils/url_reader.py",
    ],
    "caribbean": [
        "caribbean/currency_dop.py",
        "caribbean/currency_htg.py",
        "caribbean/weather_caribbean.py",
    ],
    "productivity": [
        "productivity/gmail.py",
        "productivity/calendar.py",
    ],
}


def install_tool(tool_path: str) -> bool:
    src = TOOLS_PATH / tool_path
    if not src.exists():
        print(f"  Tool not found: {tool_path}")
        return False

    dst_dir = SOFIA_PATH / "tools" / "builtin"
    if not dst_dir.exists():
        print(f"  Sofia not found at {SOFIA_PATH}")
        print("  Set SOFIA_PATH in install.py to your Sofia installation.")
        return False

    dst = dst_dir / src.name
    shutil.copy2(src, dst)
    print(f"  Installed: {src.name} -> {dst}")
    print(f"  Next: add to sofia/tools/registry.py to activate")
    return True


def install_bundle(bundle_name: str) -> None:
    if bundle_name not in BUNDLES:
        print(f"  Bundle not found: {bundle_name}")
        print(f"  Available bundles: {', '.join(BUNDLES.keys())}")
        return

    print(f"Installing bundle: {bundle_name}")
    success = 0
    for tool in BUNDLES[bundle_name]:
        if install_tool(tool):
            success += 1
    print(f"\n{success}/{len(BUNDLES[bundle_name])} tools installed.")


def list_available() -> None:
    print("Available tools:")
    for category in TOOLS_PATH.iterdir():
        if not category.is_dir() or category.name.startswith("_"):
            continue
        tools = [f.stem for f in category.glob("*.py") if not f.name.startswith("_")]
        if tools:
            print(f"  {category.name}/: {', '.join(sorted(tools))}")
    print("\nAvailable bundles:")
    for name, tools in BUNDLES.items():
        print(f"  bundle:{name} ({len(tools)} tools)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python install.py <tool_or_bundle>")
        print()
        list_available()
        sys.exit(0)

    arg = sys.argv[1]

    if arg in ("--list", "list"):
        list_available()
    elif arg.startswith("bundle:"):
        install_bundle(arg.replace("bundle:", ""))
    else:
        # Try to find the tool in any category
        found = False
        for category in TOOLS_PATH.iterdir():
            if not category.is_dir():
                continue
            candidate = category / f"{arg}.py"
            if candidate.exists():
                install_tool(f"{category.name}/{arg}.py")
                found = True
                break
        if not found:
            print(f"  Tool not found: {arg}")
            print("  Run 'python install.py list' to see available tools.")
            sys.exit(1)
