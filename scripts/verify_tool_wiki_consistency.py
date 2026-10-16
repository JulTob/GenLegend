#!/usr/bin/env python3
"""
Verify that Tool Proficiencies Wiki documentation is consistent with the code.

This script checks that:
1. All tools listed in the Wiki exist in the code
2. All tools in the code are documented in the Wiki
3. Tool attributes (ability, category) match between code and Wiki
4. No duplicate tool names exist

Run:
    python scripts/verify_tool_wiki_consistency.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from AtlasInventarium.ToolsKit import (
    TOOLS,
    ARTISAN_TOOLS,
    GAMING_SETS,
    MUSICAL_INSTRUMENTS,
    OTHER_TOOLS,
)


def extract_tools_from_wiki(wiki_path: Path) -> dict[str, dict[str, str]]:
    """
    Extract tool information from the Wiki markdown file.
    
    Returns a dict of:
    {
        "tool_name": {
            "ability": "INT",
            "category": "Artisan",
            "key": "Alchemist_Supplies"
        },
        ...
    }
    """
    if not wiki_path.exists():
        return {}
    
    content = wiki_path.read_text()
    
    # Extract from tables in the Wiki
    tools = {}
    
    # Find all tool categories and their tables
    current_category = None
    in_table = False
    
    for line in content.split('\n'):
        # Detect category headers (### Artisan's Tools (16))
        category_match = re.match(r'^###\s+([A-Za-z\s\'-]+)\s*', line)
        if category_match:
            category_name = category_match.group(1).strip()
            # Normalize category name
            category_map = {
                "Artisan's Tools": "Artisan's Tools",
                "Kits": "Kits",
                "Gaming Sets": "Gaming Sets", 
                "Musical Instruments": "Musical Instruments",
            }
            current_category = category_map.get(category_name, category_name)
            in_table = False
            continue
        
        # Detect table start
        if '| # | Name | Ability | Key |' in line:
            in_table = True
            continue
        
        # Detect table separator
        if '|---|' in line:
            continue
        
        # Extract tool rows from tables
        if in_table and current_category and line.startswith('|'):
            # Split by pipe and clean
            parts = [p.strip() for p in line.split('|') if p.strip()]
            if len(parts) >= 4:
                # parts[0] is #, parts[1] is name, parts[2] is ability, parts[3] is key
                name = parts[1]
                ability = parts[2]
                key = parts[3]
                
                # Clean up name and key (remove markdown bold and backticks)
                name = name.replace('**', '').replace('*', '').replace('`', '')
                key = key.replace('**', '').replace('*', '').replace('`', '')
                
                tools[name] = {
                    "ability": ability,
                    "category": current_category,
                    "key": key,
                }
        
        # Detect table end (empty line after table)
        if in_table and not line.strip():
            in_table = False
    
    return tools


def get_code_tools() -> dict[str, dict[str, str]]:
    """
    Extract tool information from the code.
    
    Returns a dict of:
    {
        "tool_name": {
            "ability": "INT",
            "category": "Artisan",
            "key": "Alchemist_Supplies"
        },
        ...
    }
    """
    code_tools = {}
    
    for tool in TOOLS:
        code_tools[tool.name] = {
            "ability": tool.ability,
            "category": tool.category,
            "key": tool.key,
        }
    
    return code_tools


def verify_consistency() -> tuple[bool, list[str]]:
    """
    Verify consistency between Wiki and code.
    
    Returns (success, errors) tuple.
    """
    wiki_path = PROJECT_ROOT / "Documenta" / "Wiki" / "Tool-Proficiencies.md"
    
    if not wiki_path.exists():
        return False, [f"Wiki file not found: {wiki_path}"]
    
    wiki_tools = extract_tools_from_wiki(wiki_path)
    code_tools = get_code_tools()
    
    errors = []
    
    # Check 1: All code tools are in Wiki
    code_names = set(code_tools.keys())
    wiki_names = set(wiki_tools.keys())
    
    missing_in_wiki = code_names - wiki_names
    if missing_in_wiki:
        errors.append(
            f"Tools in code but missing from Wiki ({len(missing_in_wiki)}):"
        )
        for name in sorted(missing_in_wiki):
            errors.append(f"  - {name}")
    
    # Check 2: All Wiki tools exist in code
    missing_in_code = wiki_names - code_names
    if missing_in_code:
        errors.append(
            f"Tools in Wiki but missing from code ({len(missing_in_code)}):"
        )
        for name in sorted(missing_in_code):
            errors.append(f"  - {name}")
    
    # Check 3: Attributes match for tools in both
    common_tools = code_names & wiki_names
    for name in sorted(common_tools):
        code_info = code_tools[name]
        wiki_info = wiki_tools[name]
        
        # Check ability
        if code_info["ability"] != wiki_info["ability"]:
            errors.append(
                f"Ability mismatch for '{name}': "
                f"code={code_info['ability']}, wiki={wiki_info['ability']}"
            )
        
        # Check category
        # Normalize category names for comparison
        code_category = code_info["category"]
        wiki_category = wiki_info["category"]
        
        # Handle category name variations
        category_map = {
            "Artisan's Tools": "Artisan",
            "Kits": "Kit",
            "Gaming Sets": "Gaming Set",
            "Musical Instruments": "Musical Instrument",
        }
        
        if code_category != category_map.get(wiki_category, wiki_category):
            errors.append(
                f"Category mismatch for '{name}': "
                f"code={code_category}, wiki={wiki_category}"
            )
        
        # Check key
        if code_info["key"] != wiki_info["key"]:
            errors.append(
                f"Key mismatch for '{name}': "
                f"code={code_info['key']}, wiki={wiki_info['key']}"
            )
    
    # Check 4: No duplicate tool names in code
    name_counts = {}
    for tool in TOOLS:
        name_counts[tool.name] = name_counts.get(tool.name, 0) + 1
    
    duplicates = {name: count for name, count in name_counts.items() if count > 1}
    if duplicates:
        errors.append(
            f"Duplicate tool names in code ({len(duplicates)}):"
        )
        for name, count in sorted(duplicates.items()):
            errors.append(f"  - {name} (appears {count} times)")
    
    # Check 5: Verify counts match
    wiki_count = len(wiki_tools)
    code_count = len(code_tools)
    
    if wiki_count != code_count:
        errors.append(
            f"Tool count mismatch: Wiki={wiki_count}, Code={code_count}"
        )
    
    return (len(errors) == 0, errors)


def main() -> int:
    """Run verification and report results."""
    print("=" * 70)
    print("Tool Proficiencies Wiki-Consistency Verification")
    print("=" * 70)
    print()
    
    success, errors = verify_consistency()
    
    if success:
        print("✅ All Tool Proficiencies Wiki documentation is consistent with code.")
        print()
        print("Summary:")
        print(f"  - Tools in code: {len(TOOLS)}")
        print(f"  - Artisan Tools: {len(ARTISAN_TOOLS)}")
        print(f"  - Gaming Sets: {len(GAMING_SETS)}")
        print(f"  - Musical Instruments: {len(MUSICAL_INSTRUMENTS)}")
        print(f"  - Other Tools (Kits): {len(OTHER_TOOLS)}")
        return 0
    else:
        print("❌ Wiki-Consistency verification FAILED:")
        for error in errors:
            print(f"  {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
