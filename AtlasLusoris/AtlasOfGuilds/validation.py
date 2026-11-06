"""Validation utilities for Guild Specializations.

This module provides runtime validation that ensures:
1. Every Guild has at least one Specialization
2. Specializations are registered under known Guilds
3. No two Guilds share a Specialization name, so the UI picker
   never offers an ambiguous or incomplete Guild

Run standalone: python -m AtlasLusoris.AtlasOfGuilds.validation
"""

from __future__ import annotations

import sys


def validate_all_guilds_have_specializations(
		guilds: dict[str, type],
		specializations_by_guild: dict[str, tuple[str, ...]],
		) -> tuple[bool, list[str]]:
	"""
	Verify that every Guild has at least one Specialization.

	Args:
	guilds: Mapping of guild names to guild classes (e.g., GUILDS)
	specializations_by_guild: Mapping of guild names to their specializations

	Returns:
	(success, errors) tuple where success is True if all Guilds have specializations,
	and errors is a list of error messages if any Guilds are missing specializations.
	"""
	errors = []
	for guild_name in sorted(guilds.keys()):
		specializations = specializations_by_guild.get(guild_name, ())
		if not specializations:
			errors.append(
				f"Guild '{guild_name}' has NO specializations. "
				f"The UI picker must not offer this Guild until it has at least one."
				)

	return (len(errors) == 0, errors)


def validate_specializations_belong_to_guilds(
		guilds: dict[str, type],
		specializations_by_guild: dict[str, tuple[str, ...]],
		) -> tuple[bool, list[str]]:
	"""
	Verify that every registered Specialization belongs to a known Guild.

	Args:
	guilds: Mapping of guild names to guild classes
	specializations_by_guild: Mapping of guild names to their specializations

	Returns:
	(success, errors) tuple where success is True if every registered
	Specialization sits under a known Guild, and errors lists any
	Specializations registered under unknown Guilds.
	"""
	errors = []
	for guild_name in sorted(specializations_by_guild.keys()):
		if guild_name not in guilds:
			errors.append(
				f"Specializations registered under unknown Guild '{guild_name}': "
				f"{specializations_by_guild[guild_name]}"
				)

	return (len(errors) == 0, errors)


def validate_no_duplicate_specialization_names(
		specializations_by_guild: dict[str, tuple[str, ...]],
		) -> tuple[bool, list[str]]:
	"""
	Verify that no two Guilds share the same Specialization name.

	Args:
	specializations_by_guild: Mapping of guild names to their specializations

	Returns:
	(success, errors) tuple where success is True if all Specialization names are unique,
	and errors is a list of error messages for any duplicates found.
	"""
	errors = []
	first_seen: dict[str, str] = {}

	for guild_name, specializations in specializations_by_guild.items():
		for spec_name in specializations:
			if spec_name in first_seen:
				errors.append(
					f"Duplicate Specialization name '{spec_name}' "
					f"(first in Guild '{first_seen[spec_name]}', now in '{guild_name}'). "
					f"Each Specialization name must be unique across all Guilds."
					)
			else:
				first_seen[spec_name] = guild_name

	return (len(errors) == 0, errors)


def validate_specialization_registration(
		guilds: dict[str, type],
		specializations_by_guild: dict[str, tuple[str, ...]],
		) -> tuple[bool, list[str]]:
	"""
	Run all Guild Specialization validation checks.

	Args:
	guilds: Mapping of guild names to guild classes
	specializations_by_guild: Mapping of guild names to their specializations

	Returns:
	(success, all_errors) tuple where success is True only if all checks pass,
	and all_errors is a concatenated list of all error messages.
	"""
	all_errors = []

	# Check 1: All Guilds have specializations
	success, errors = validate_all_guilds_have_specializations(
		guilds, specializations_by_guild
	)
	if not success:
		all_errors.extend(errors)

	# Check 2: Specializations belong to known Guilds
	success, errors = validate_specializations_belong_to_guilds(
		guilds, specializations_by_guild
	)
	if not success:
		all_errors.extend(errors)

	# Check 3: No duplicate Specialization names
	success, errors = validate_no_duplicate_specialization_names(
		specializations_by_guild
	)
	if not success:
		all_errors.extend(errors)

	return (len(all_errors) == 0, all_errors)


def assert_guild_specializations_valid(
		guilds: dict[str, type],
		specializations_by_guild: dict[str, tuple[str, ...]],
		) -> None:
	"""
	Assert that Guild Specializations are valid.

	Raises AssertionError if any validation check fails.

	Args:
	guilds: Mapping of guild names to guild classes
	specializations_by_guild: Mapping of guild names to their specializations
	"""
	success, errors = validate_specialization_registration(
		guilds, specializations_by_guild
	)
	if not success:
		error_msg = "Guild Specialization validation FAILED:\n"
		for error in errors:
			error_msg += f"  - {error}\n"
		raise AssertionError(error_msg)


if __name__ == "__main__":
	# Standalone execution: run validation and report results
	from AtlasLusoris.GuildKit import GUILDS
	from AtlasLusoris.Grimoire_of_Guilds import SPECIALIZATIONS_BY_GUILD

	print("=" * 70)
	print("Guild Specialization Validation (Standalone)")
	print("=" * 70)
	print()

	success, errors = validate_specialization_registration(
		dict(GUILDS), dict(SPECIALIZATIONS_BY_GUILD)
	)

	if success:
		print("OK — all Guild Specialization validations PASSED.")
		sys.exit(0)
	else:
		print("Guild Specialization validation FAILED:")
		for error in errors:
			print(f"  - {error}")
		sys.exit(1)
