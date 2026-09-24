"""
Equipment invariant harness — the ALL GREEN gate for the Starting Equipment quests.

Run:  PYTHONPATH=. STRICT_GENERATION=1 .venv/bin/python3 scripts/verify_equipment.py

Gates the GearKit system (Grimoire_of_Items + Ledgers + Crafts + the weapon
mastery bridge), which replaced the legacy Inventory as the live loadout source.

Invariants checked
	1. Ledger record integrity — value and weight are not transposed.
	2. No accidental duplicates in the bag. Consumables are EXEMPT: carrying
	   four potions is the point, not a bug.
	3. Purse is non-negative and floored to the copper piece.
	4. AC is DERIVED and agrees with what is actually worn: it never exceeds
	   best-of(worn armour, Unarmored Defence) + shield + magical grants.
	5. Body slots respect their capacity (one hat, one cloak, three rings).
	6. A Character only wields weapons their Guild trained them for, and
	   never a firearm.
	7. Armour worn is within the Guild's armour training.
	8. Unarmored Defence that armour would void (Monk, Dance) stays unarmoured.
	9. Every equipped item is actually owned.
	10. Weapon Mastery: the right COUNT, every mastered weapon is CARRIED,
	    melee-only Guilds never master a non-Thrown ranged weapon, and the
	    drills are balanced between reach and close work.
	11. No duplicate chip labels on the sheet.
	12. Generation is deterministic per seed.
"""

from __future__ import annotations

import collections
import contextlib
import os
import sys


GUILDS_UNDER_TEST = (
		"Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
		"Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
		)
LEVELS = (1, 3, 5, 10, 20)

# Generation is slow (~0.5 s/character), so the default sweep stays gate-sized.
# EQUIPMENT_SEEDS=20 for a deep sweep before closing a quest.
SEEDS = range(
		int(
				os.environ.get(
						"EQUIPMENT_SEEDS",
						3,
						)
				)
		)


@contextlib.contextmanager
def hush():
	"""Silence the generator's decorator trace logs at the fd level."""
	with open(os.devnull, "w") as devnull:
		out, err = os.dup(1), os.dup(2)
		os.dup2(devnull.fileno(), 1)
		os.dup2(devnull.fileno(), 2)
		try:
			yield
		finally:
			os.dup2(out, 1)
			os.dup2(err, 2)
			os.close(out)
			os.close(err)


def check_records(failures):
	"""Ledger records must not transpose value and weight."""
	from AtlasInventarium.Ledger_of_Armors import Chain_Mail
	from AtlasInventarium.Ledger_of_Weapons import Longsword

	if (Chain_Mail.value, Chain_Mail.weight) != (75, 55):
		failures.append(
				f"record: Chain Mail value/weight wrong "
				f"(value={Chain_Mail.value}, weight={Chain_Mail.weight}; expected 75/55)"
				)

	if (Longsword.value, Longsword.weight) != (15, 3):
		failures.append(
				f"record: Longsword value/weight wrong "
				f"(value={Longsword.value}, weight={Longsword.weight}; expected 15/3)"
				)


def check_character(char, guild, level, seed, failures):
	from AtlasInventarium.GearKit import (
			armour_allowance,
			current_armour_class,
			unarmoured_formula,
			weapon_pool,
			)
	from AtlasInventarium.Map_of_Gear_Proficiency import (
			unarmoured_refuses_armour,
			unarmoured_refuses_shield,
			)
	from AtlasInventarium.Grimoire_of_Items import (
			SLOTS,
			Consumable,
			Firearm,
			Weapon,
			carried,
			equipped,
			grant_total,
			owned,
			)
	from AtlasLusoris.Map_of_Weapon_Masteries import (
			_melee_only,
			_reaches_far,
			mastery_count,
			)

	def fail(message):
		failures.append(
				f"{guild} L{level} seed{seed}: {message}"
				)

	loadout = char.equipment

	# --- bag has no accidental duplicates (consumables may repeat) ---------
	names = [
			item.name
			for item in carried(char)
			if item not in Consumable
			]
	duplicates = [
			name
			for name, count in collections.Counter(names).items()
			if count > 1
			]
	if duplicates:
		fail(
				f"duplicate bag items {duplicates}"
				)

	# --- purse -------------------------------------------------------------
	purse = loadout.purse
	if purse < 0:
		fail(
				f"negative purse {purse}"
				)
	# Compare with a tolerance: 139.8 * 100 is 13980.000000000002 in binary
	# floating point, so an exact equality here reports false failures.
	if abs(purse * 100 - round(purse * 100)) > 1e-6:
		fail(
				f"purse {purse} is finer than a copper piece"
				)

	# --- slot capacities ---------------------------------------------------
	for tag, capacity in SLOTS:
		in_use = equipped(
				char,
				tag,
				)
		if len(in_use) > capacity:
			fail(
					f"{len(in_use)} items in the {tag.NAME} slot (capacity {capacity})"
					)

	# --- AC is derived and never exceeds what is worn ----------------------
	worn = loadout.wearing
	shield_bonus = 2 if loadout.offhand is not None else 0
	natural = unarmoured_formula(char)

	def modifier(score):
		return (score - 10) // 2

	ceiling = natural
	if worn is not None:
		cap = worn.dex_cap
		dexterity = modifier(char.AS.DEX)
		allowed = dexterity if cap is None else min(dexterity, cap)
		ceiling = max(
				ceiling,
				worn.base_ac + allowed,
				)
	ceiling += shield_bonus + grant_total(char, "AC")

	derived = current_armour_class(char)
	if derived != ceiling:
		fail(
				f"AC {derived} != derived ceiling {ceiling} "
				f"(worn={getattr(worn, 'called', 'nothing')}, "
				f"shield={shield_bonus}, natural={natural})"
				)
	if char.AC != derived:
		fail(
				f"char.AC {char.AC} out of step with derived AC {derived}"
				)

	# --- weapons are trained ones, never firearms --------------------------
	allowed_weapons = {
			weapon.name
			for weapon in weapon_pool(char)
			}
	for weapon in equipped(
			char,
			Weapon,
			):
		if weapon.name not in allowed_weapons:
			fail(
					f"wields untrained {weapon.called}"
					)
		if weapon in Firearm:
			fail(
					f"was handed a firearm ({weapon.called})"
					)

	# --- armour is within training -----------------------------------------
	if worn is not None:
		allowance = armour_allowance(char)
		if worn.armour_kind not in allowance:
			fail(
					f"wears {worn.armour_kind} armour but is trained for {allowance}"
					)

	# --- Unarmored Defense: no armour; a Shield only if its source allows --
	if worn is not None and unarmoured_refuses_armour(char):
		fail(
				f"{worn.called} worn over Unarmored Defense"
				)
	if loadout.offhand is not None and unarmoured_refuses_shield(char):
		fail(
				"shield carried, voiding Unarmored Defense"
				)

	# --- everything equipped is owned --------------------------------------
	holdings = owned(char)
	for item in equipped(char):
		if item not in holdings:
			fail(
					f"{item.called} is equipped but not owned"
					)

	# --- weapon mastery bridge ---------------------------------------------
	picks = list(
			getattr(
					char,
					"weapon_mastery_picks",
					None,
					) or []
			)
	expected_count = mastery_count(char)
	if len(picks) != expected_count:
		fail(
				f"{len(picks)} weapon masteries, expected {expected_count}"
				)

	owned_names = {
			item.name
			for item in owned(char)
			}
	for weapon_name, _mastery in picks:
		# A drill you cannot practise is a line of text about nothing.
		if weapon_name not in owned_names:
			fail(
					f"mastered {weapon_name} but does not carry one"
					)
		if weapon_name not in allowed_weapons:
			fail(
					f"mastered untrained weapon {weapon_name}"
					)
		if _melee_only(char):
			from AtlasInventarium.Grimoire_of_Items import Melee
			from AtlasInventarium.Ledger_of_Weapons import WEAPONS_BY_NAME

			record = WEAPONS_BY_NAME.get(weapon_name)
			if record is not None and record not in Melee:
				fail(
						f"melee-only Guild mastered ranged {weapon_name}"
						)

	# Balance: at least floor(n/2) of the drills should reach (Ranged or
	# Thrown), so a hero is never left unable to answer a distant foe.
	if picks:
		far = sum(
				1
				for weapon_name, _m in picks
				if _reaches_far(weapon_name)
				)
		if far < len(picks) // 2:
			fail(
					f"only {far} of {len(picks)} masteries reach far "
					f"(want at least {len(picks) // 2})"
					)

	# --- no duplicate chip labels on the sheet ------------------------------
	chip_labels = [
			chip[0]
			for feature in char.features
			for chip in getattr(feature, "chips", ())
			]
	chip_dupes = [
			label
			for label, count in collections.Counter(chip_labels).items()
			if count > 1
			]
	if chip_dupes:
		fail(
				f"duplicate sheet chips {chip_dupes}"
				)


def main():
	failures: list[str] = []

	with hush():
		from AtlasActorLudi.Map_of_Character_Generation import summon_player

		check_records(failures)

		count = 0
		for guild in GUILDS_UNDER_TEST:
			for level in LEVELS:
				for seed in SEEDS:
					char = summon_player(
							guild=guild,
							level=level,
							seed=seed,
							)
					check_character(
							char,
							guild,
							level,
							seed,
							failures,
							)
					count += 1

		# --- determinism ---------------------------------------------------
		first = summon_player(guild="Fighter", level=7, seed=4242)
		again = summon_player(guild="Fighter", level=7, seed=4242)
		signature = lambda c: (
				c.AC,
				float(c.equipment.purse),
				sorted(i.called for i in c.equipment.bag),
				getattr(c.equipment.melee, "called", None),
				getattr(c.equipment.ranged, "called", None),
				getattr(c.equipment.wearing, "called", None),
				tuple(getattr(c, "weapon_mastery_picks", ()) or ()),
				)
		if signature(first) != signature(again):
			failures.append(
					"determinism: same seed produced different equipment"
					)

	print(
			f"Checked {count} characters "
			f"({len(GUILDS_UNDER_TEST)} guilds x {len(LEVELS)} levels x {len(SEEDS)} seeds)"
			)

	if failures:
		print(
				f"\n{len(failures)} FAILURES:"
				)
		for line in failures[:40]:
			print(
					f"  ! {line}"
					)
		if len(failures) > 40:
			print(
					f"  ... and {len(failures) - 40} more"
					)
		sys.exit(1)

	print(
			"\nALL GREEN — equipment invariants hold."
			)


if __name__ == "__main__":
	main()
