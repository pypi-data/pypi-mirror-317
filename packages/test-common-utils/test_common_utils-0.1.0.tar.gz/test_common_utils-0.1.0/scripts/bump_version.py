#!/usr/bin/env python3
import re
import sys
from pathlib import Path
from typing import Literal, Optional

VersionType = Literal["major", "minor", "patch"]


def bump_version(version_type: VersionType, current_version: str) -> str:
    major, minor, patch = map(int, current_version.split("."))

    if version_type == "major":
        return f"{major + 1}.0.0"
    elif version_type == "minor":
        return f"{major}.{minor + 1}.0"
    else:  # patch
        return f"{major}.{minor}.{patch + 1}"


def update_version(version_type: VersionType) -> None:
    # Update version in pyproject.toml
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text()
    version_match = re.search(r'version = "(\d+\.\d+\.\d+)"', content)

    if not version_match:
        print("Could not find version in pyproject.toml")
        sys.exit(1)

    current_version = version_match.group(1)
    new_version = bump_version(version_type, current_version)
    new_content = content.replace(
        f'version = "{current_version}"', f'version = "{new_version}"'
    )
    pyproject_path.write_text(new_content)

    # Update version in __init__.py
    init_path = Path("src/__init__.py")
    content = init_path.read_text()
    new_content = re.sub(
        r'__version__ = "\d+\.\d+\.\d+"', f'__version__ = "{new_version}"', content
    )
    init_path.write_text(new_content)

    print(f"Bumped version from {current_version} to {new_version}")
    print(f"Don't forget to:")
    print(f"1. git add pyproject.toml src/__init__.py")
    print(f"2. git commit -m 'Bump version to {new_version}'")
    print(f"3. git tag v{new_version}")
    print(f"4. git push && git push --tags")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in ("major", "minor", "patch"):
        print("Usage: python scripts/bump_version.py [major|minor|patch]")
        sys.exit(1)

    update_version(sys.argv[1])
