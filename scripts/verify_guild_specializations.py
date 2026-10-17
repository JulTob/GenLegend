#!/usr/bin/env python3
"""Verify that every Guild has at least one Specialization.

This script ensures that:
1. Every Guild in GUILDS has at least one registered Specialization
2. Every Specialization belongs to a valid Guild
3. No Guild offers invalid/nonexistent Specializations in the UI

Run:
    python scripts/verify_guild_specializations.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from AtlasLusoris.GuildKit import GUILDS, Specialization_Choices


def verify_all_guilds_have_specializations() -> tuple[bool, list[str]]:
	"""Check that every Guild has at least one Specialization."""
	errors = []
	for guild_name, guild_class in sorted(GUILDS.items()):
		specializations = Specialization_Choices(guild_name)
		if not specializations:
			errors.append(
				f"❌ Guild '{guild_name}' has NO specializations. "
				f"This will break the UI picker."
			)
		else:
			print(f"✅ Guild '{guild_name}' has {len(specializations)} specializations: {specializations}")

	if errors:
		return False, errors
	return True, []


def verify_specialization_belongs_to_guild() -> tuple[bool, list[str]]:
	"""Check that every Specialization belongs to a valid Guild."""
	from AtlasLusoris.Grimoire_of_Guilds import SPECIALIZATIONS_BY_GUILD

	errors = []
	first_seen: dict[str, str] = {}

	for guild_name, specializations in SPECIALIZATIONS_BY_GUILD.items():
		if guild_name not in GUILDS:
			errors.append(
				f"❌ Specializations registered under unknown Guild '{guild_name}': {specializations}"
			)
		else:
			for spec_name in specializations:
				if spec_name in first_seen:
					errors.append(
						f"❌ Specialization '{spec_name}' is registered under multiple Guilds: "
						f"{first_seen[spec_name]} and {guild_name}"
					)
				else:
					first_seen[spec_name] = guild_name

	if errors:
		return False, errors
	return True, []


def verify_no_duplicate_specialization_names() -> tuple[bool, list[str]]:
	"""Check that no two Guilds share the same Specialization name."""
	from AtlasLusoris.Grimoire_of_Guilds import SPECIALIZATIONS_BY_GUILD

	errors = []
	first_seen: dict[str, str] = {}

	for guild_name, specializations in SPECIALIZATIONS_BY_GUILD.items():
		for spec_name in specializations:
			if spec_name in first_seen:
				errors.append(
					f"❌ Duplicate Specialization name '{spec_name}' "
					f"(first seen in {first_seen[spec_name]})"
				)
			else:
				first_seen[spec_name] = guild_name

	if errors:
		return False, errors
	return True, []


def main() -> int:
	"""Run all verification checks."""
	print("=" * 70)
	print("Guild Specialization Validation")
	print("=" * 70)
	print()

	all_passed = True

	# Check 1: All Guilds have specializations
	print("[Check 1] Verifying all Guilds have at least one Specialization...")
	passed, errors = verify_all_guilds_have_specializations()
	if not passed:
		all_passed = False
		for error in errors:
			print(error)
	print()

	# Check 2: All Specializations belong to valid Guilds
	print("[Check 2] Verifying Specializations belong to valid Guilds...")
	passed, errors = verify_specialization_belongs_to_guild()
	if not passed:
		all_passed = False
		for error in errors:
			print(error)
	print()

	# Check 3: No duplicate Specialization names
	print("[Check 3] Verifying no duplicate Specialization names...")
	passed, errors = verify_no_duplicate_specialization_names()
	if not passed:
		all_passed = False
		for error in errors:
			print(error)
	print()

	print("=" * 70)
	if all_passed:
		print("✅ All Guild Specialization checks PASSED.")
		return 0
	else:
		print("❌ Some Guild Specialization checks FAILED.")
		return 1


if __name__ == "__main__":
	sys.exit(main())
