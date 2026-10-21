#!/usr/bin/env python3
"""Verify that every Guild has at least one Specialization.

The registry checks live in AtlasLusoris.AtlasOfGuilds.validation — the
same module GuildKit.py runs at startup — so CI and the application
exercise one implementation. This wrapper adds the UI-facing check:
Specialization_Choices() must offer at least one Specialization per Guild.

Run:
    python scripts/verify_guild_specializations.py
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
	sys.path.insert(0, str(PROJECT_ROOT))

from AtlasLusoris.AtlasOfGuilds.validation import (
	validate_specialization_registration,
	)
from AtlasLusoris.Grimoire_of_Guilds import SPECIALIZATIONS_BY_GUILD
from AtlasLusoris.GuildKit import GUILDS, Specialization_Choices


def verify_ui_offers_specializations() -> tuple[bool, list[str]]:
	"""Check that the UI picker can offer a Specialization for every Guild."""
	errors = []
	for guild_name in sorted(GUILDS):
		specializations = Specialization_Choices(guild_name)
		if not specializations:
			errors.append(
				f"Guild '{guild_name}' offers NO specializations through "
				f"Specialization_Choices(). This will break the UI picker."
				)
		else:
			print(
				f"Guild '{guild_name}' offers {len(specializations)} "
				f"specializations: {specializations}"
				)
	return (len(errors) == 0, errors)


def main() -> int:
	"""Run all verification checks."""
	print("=" * 70)
	print("Guild Specialization Validation")
	print("=" * 70)
	print()

	all_passed = True

	# Check 1: registry integrity (shared with the GuildKit startup check)
	print("[Check 1] Registry: every Guild has Specializations, all registered under known Guilds, no duplicates...")
	passed, errors = validate_specialization_registration(
		dict(GUILDS), dict(SPECIALIZATIONS_BY_GUILD)
		)
	if not passed:
		all_passed = False
		for error in errors:
			print(f"  {error}")
	print()

	# Check 2: the UI picker agrees with the registry
	print("[Check 2] UI: Specialization_Choices() offers a Specialization for every Guild...")
	passed, errors = verify_ui_offers_specializations()
	if not passed:
		all_passed = False
		for error in errors:
			print(f"  {error}")
	print()

	print("=" * 70)
	if all_passed:
		print("All Guild Specialization checks PASSED.")
		return 0
	print("Some Guild Specialization checks FAILED.")
	return 1


if __name__ == "__main__":
	sys.exit(main())
