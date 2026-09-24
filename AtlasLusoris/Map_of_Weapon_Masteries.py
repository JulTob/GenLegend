"""
Weapon Mastery catalogue — pick weapons and resolve mastery text.

Used by Training Entries so the sheet names the weapons this Character
trained, not a blank "choose 2" rule dump.
"""

from __future__ import annotations

import random
from typing import Any

from TopKit import Pre, Tag

from AtlasActorLudi.CharactersKit import Report_Of


class Weapon_Mastery(Tag):
	"""
	Root of "this hero has drilled with a Longsword".

	A mastery is a Tag on the CHARACTER, minted per weapon
	(``Mastery_Of_Longsword``). Being a Tag rather than a list entry means
	the rest of the system can simply ask — and, in particular, the loadout
	can go and buy the weapons the hero trained on.
	"""

	NAME = "Weapon Mastery"

	@Pre
	def Character_Only(
			target,
			):
		from AtlasActorLudi.CharactersKit import Character
		return isinstance(
				target,
				Character,
				)


_MASTERY_TAGS: dict[str, type[Weapon_Mastery]] = {}

from TopKit import Pre, Tag


class Weapon_Mastery(Tag):
	"""
	Root of "this hero has drilled with a Longsword".

	A mastery is a Tag on the CHARACTER, minted per weapon
	(``Mastery_Of_Longsword``). Being a Tag rather than a list entry means
	the rest of the system can simply ask — and, in particular, the loadout
	can go and buy the weapons the hero trained on.
	"""

	NAME = "Weapon Mastery"

	@Pre
	def Character_Only(
			target,
			):
		from AtlasActorLudi.CharactersKit import Character
		return isinstance(
				target,
				Character,
				)


_MASTERY_TAGS: dict[str, type[Weapon_Mastery]] = {}


# PHB 2024 Simple + Martial weapons with their mastery property.
WEAPON_MASTERIES: dict[str, str] = {
		"Club": "Slow",
		"Dagger": "Nick",
		"Greatclub": "Push",
		"Handaxe": "Vex",
		"Javelin": "Slow",
		"Light Hammer": "Nick",
		"Mace": "Sap",
		"Quarterstaff": "Topple",
		"Sickle": "Nick",
		"Spear": "Sap",
		"Light Crossbow": "Slow",
		"Dart": "Vex",
		"Shortbow": "Vex",
		"Sling": "Slow",
		"Battleaxe": "Topple",
		"Flail": "Sap",
		"Glaive": "Graze",
		"Greataxe": "Cleave",
		"Greatsword": "Graze",
		"Halberd": "Cleave",
		"Lance": "Topple",
		"Longsword": "Sap",
		"Maul": "Topple",
		"Morningstar": "Sap",
		"Pike": "Push",
		"Rapier": "Vex",
		"Scimitar": "Nick",
		"Shortsword": "Vex",
		"Trident": "Topple",
		"Warhammer": "Push",
		"War Pick": "Sap",
		"Whip": "Slow",
		"Blowgun": "Vex",
		"Hand Crossbow": "Vex",
		"Heavy Crossbow": "Push",
		"Longbow": "Slow",
		"Musket": "Slow",
		"Pistol": "Vex",
		}

MASTERY_TEXT: dict[str, str] = {
		"Cleave": (
			"After you hit, you may make one extra melee attack against a "
			"second creature within 5 feet of the first (once per turn; "
			"no ability modifier to that damage)."
			),
		"Graze": (
			"If your attack roll misses, the target still takes damage "
			"equal to the ability modifier you used for the attack."
			),
		"Nick": (
			"The Light-property extra attack can be made during the Attack "
			"action instead of as a Bonus Action (once per turn)."
			),
		"Push": (
			"On a hit you may push the target (Large or smaller) up to "
			"10 feet straight away from you."
			),
		"Sap": (
			"On a hit the target has Disadvantage on its next attack roll "
			"before the start of your next turn."
			),
		"Slow": (
			"On a hit the target's Speed is reduced by 10 feet until the "
			"start of your next turn."
			),
		"Topple": (
			"On a hit you may force a Constitution saving throw "
			"<b>(DC {dc})</b>; on a failure the target falls Prone."
			),
		"Vex": (
			"On a hit you have Advantage on your next attack roll against "
			"that creature before the end of your next turn."
			),
		}


def mastery_for(
		weapon: str,
		) -> str:
	return WEAPON_MASTERIES[weapon]


def mastery_save_dc(
		char: Any,
		) -> int:
	"""
	The DC a mastery property imposes: 8 + Proficiency Bonus + the modifier.

	The modifier is the better of Strength and Dexterity, because that is the
	one a Character will be attacking with: a melee weapon uses Strength unless
	it has Finesse, and nobody takes the worse of the two on purpose.
	"""
	scores = getattr(
			char,
			"AS",
			None,
			)
	best = max(
			int(
				getattr(
					scores,
					"str_mod",
					0,
					) or 0
				),
			int(
				getattr(
					scores,
					"dex_mod",
					0,
					) or 0
				),
			)
	proficiency = int(
			getattr(
				char,
				"proficiency_bonus",
				2,
				) or 2
			)
	return 8 + proficiency + best


def mastery_blurb(
		mastery: str,
		char: Any = None,
		) -> str:
	"""
	The mastery's rules line, with any resolved value filled in.

	Only Topple carries a slot today.  The Character is optional so that the
	catalogue can still be read without one, but the sheet always passes it:
	printing a formula where a number belongs is what the house rule forbids.
	"""
	text = MASTERY_TEXT.get(
			mastery,
			"",
			)

	if "{dc}" in text and char is not None:
		text = text.replace(
				"{dc}",
				str(
					mastery_save_dc(
						char
						)
					),
				)
	return text


def _mastery_stream(
		char: Any,
		):
	"""Use one Character Dice Bag so a seed repeats the same drills."""
	if hasattr(
		char,
		"Dice_Bag",
		):
		return char.Dice_Bag(
			"fighter.weapon_masteries",
			version="2024",
			namespace="GenLegendFighter",
			)
	seed = getattr(
			char,
			"seed",
			None,
			)
	if seed is None:
		seed = getattr(
				char,
				"name",
				"",
				) or 0
	return random.Random(
			f"{seed}:weapon_masteries"
			)


# 2024 PHB: Barbarian and Paladin train Weapon Mastery on Melee weapons only.
# Fighter, Ranger and Rogue may drill with anything they are proficient in.
_MELEE_ONLY_GUILDS = (
		"Barbarian",
		"Paladin",
		)


def _melee_only(
		char: Any,
		) -> bool:
	return getattr(
			char,
			"char_class",
			None,
			) in _MELEE_ONLY_GUILDS


# How many weapons each Guild drills, by level (index 0 unused).
_PROGRESSION: dict[str, tuple[int, ...]] = {
		"Barbarian": (
				0,
				2, 2, 2, 3, 3, 3, 3, 3, 3, 4,
				4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
				),
		}
_FLAT_PROGRESSION = {
		"Paladin": 2,
		"Ranger": 2,
		"Rogue": 2,
		}


def mastery_count(
		char: Any,
		) -> int:
	"""How many weapons this Character drills, from their Guild and level."""
	guild = getattr(
			char,
			"char_class",
			None,
			)
	level = max(
			1,
			min(
					20,
					int(
							getattr(
									char,
									"level",
									1,
									) or 1
							),
					),
			)

	table = _PROGRESSION.get(
			guild
			)
	if table is not None:
		return table[level]
	if guild == "Fighter":
		from AtlasLusoris.AtlasOfGuilds.FighterKit import Fighter

		choice = next(
			choice
			for choice in Fighter.CHOICES
			if choice.name == "Weapon Mastery"
			)
		return choice.total_at(
			level
			)
	return _FLAT_PROGRESSION.get(
			guild,
			0,
			)


def _mastery_tag(
		weapon: str,
	):
	"""Get or mint the Tag that says "this hero has mastered a Longsword"."""
	from TopKit import Tag

	class_name = "Mastery_Of_" + "".join(
			part.capitalize()
			for part in weapon.replace(
					"-",
					" ",
					).replace(
					"'",
					"",
					).split()
			)

	existing = _MASTERY_TAGS.get(
			class_name
			)
	if existing is not None:
		return existing

	tag = type(
			class_name,
			(
					Weapon_Mastery,
					),
			{
					"NAME": f"{weapon} Mastery",
					"WEAPON": Report_Of(
							weapon
							),
					"MASTERY": Report_Of(
							WEAPON_MASTERIES[weapon]
							),
					"__module__": __name__,
					},
			)
	_MASTERY_TAGS[class_name] = tag
	return tag


def mastered_tags(
		char: Any,
		) -> tuple:
	"""Every weapon-mastery Tag this Character carries."""
	return tuple(
			tag
			for tag in _MASTERY_TAGS.values()
			if char in tag
			)


# How many weapons each Guild drills, by level (index 0 unused).
_PROGRESSION: dict[str, tuple[int, ...]] = {
		"Fighter": (
				0,
				3, 3, 3, 4, 4, 4, 4, 4, 4, 5,
				5, 5, 5, 5, 5, 6, 6, 6, 6, 6,
				),
		"Barbarian": (
				0,
				2, 2, 2, 3, 3, 3, 3, 3, 3, 4,
				4, 4, 4, 4, 4, 4, 4, 4, 4, 4,
				),
		}
_FLAT_PROGRESSION = {
		"Paladin": 2,
		"Ranger": 2,
		"Rogue": 2,
		}


def mastery_count(
		char: Any,
		) -> int:
	"""How many weapons this Character drills, from their Guild and level."""
	guild = getattr(
			char,
			"char_class",
			None,
			)
	level = max(
			1,
			min(
					20,
					int(
							getattr(
									char,
									"level",
									1,
									) or 1
							),
					),
			)

	table = _PROGRESSION.get(
			guild
			)
	if table is not None:
		return table[level]
	return _FLAT_PROGRESSION.get(
			guild,
			0,
			)


def _mastery_tag(
		weapon: str,
	):
	"""Get or mint the Tag that says "this hero has mastered a Longsword"."""
	from TopKit import Tag

	class_name = "Mastery_Of_" + "".join(
			part.capitalize()
			for part in weapon.replace(
					"-",
					" ",
					).replace(
					"'",
					"",
					).split()
			)

	existing = _MASTERY_TAGS.get(
			class_name
			)
	if existing is not None:
		return existing

	tag = type(
			class_name,
			(
					Weapon_Mastery,
					),
			{
					"NAME": f"{weapon} Mastery",
					"WEAPON": Report_Of(
							weapon
							),
					"MASTERY": Report_Of(
							WEAPON_MASTERIES[weapon]
							),
					"__module__": __name__,
					},
			)
	_MASTERY_TAGS[class_name] = tag
	return tag


def mastered_tags(
		char: Any,
		) -> tuple:
	"""Every weapon-mastery Tag this Character carries."""
	return tuple(
			tag
			for tag in _MASTERY_TAGS.values()
			if char in tag
			)


def mastery_candidates(
		char: Any,
		) -> list[str]:
	"""
	Weapons this Character could master, best candidates FIRST.

	The order is the whole point: a Character masters the weapon in their
	hands before one they merely own, and one they own before a weapon they
	have only ever read about. Everything is filtered down to what their
	Guild actually trained them to hold, so a Rogue never masters a Greataxe.
	"""
	allowed: set[str] = set()
	try:
		from AtlasInventarium.GearKit import weapon_pool
		from AtlasInventarium.ItemKit import Melee

		melee_only = _melee_only(
				char
				)
		# Filter the WHOLE catalogue here, not just the weapons already in
		# hand — otherwise a Barbarian fills their remaining drills from the
		# ranged rack they are not allowed to train with.
		allowed = {
				weapon.name
				for weapon in weapon_pool(
						char
						)
				if weapon.name in WEAPON_MASTERIES
				and (
					weapon in Melee
					or not melee_only
					)
				}
	except Exception:
		allowed = set(
				WEAPON_MASTERIES
				)

	equipped_names: list[str] = []
	carried_names: list[str] = []
	try:
		from AtlasInventarium.ItemKit import (
				Melee,
				Weapon,
				carried,
				equipped,
				)

		def usable(item):
			if item not in Weapon:
				return False
			if _melee_only(
					char
					) and item not in Melee:
				return False
			return item.name in allowed

		equipped_names = [
				item.name
				for item in equipped(
						char,
						)
				if usable(
						item
						)
				]
		carried_names = [
				item.name
				for item in carried(
						char
						)
				if usable(
						item
						)
				]
	except Exception:
		pass

	rest = sorted(
			allowed - set(
					equipped_names
					) - set(
					carried_names
					)
			)
	_mastery_stream(
			char
			).shuffle(
			rest
			)

	ordered: list[str] = []
	for name in [
			*equipped_names,
			*carried_names,
			*rest,
			]:
		if name not in ordered:
			ordered.append(
					name
					)
	return ordered


def _reaches_far(
		weapon: str,
		) -> bool:
	"""
	True for weapons that can strike at range — including THROWN ones.

	A hero who trained to throw a Handaxe has a ranged option even though
	the axe is a Melee weapon, so Thrown counts toward the ranged half.
	"""
	try:
		from AtlasInventarium.ItemKit import Ranged
		from AtlasInventarium.Ledger_of_Weapons import WEAPONS_BY_NAME

		record = WEAPONS_BY_NAME.get(
				weapon
				)
		if record is None:
			return False
		if record in Ranged:
			return True
		return any(
				str(
						prop
						).startswith(
						"Thrown"
						)
				for prop in record.properties
				)
	except Exception:
		return False


def pick_weapon_masteries(
		char: Any,
		n: int,
		) -> list[tuple[str, str]]:
	"""
	Choose ``n`` distinct weapons and return ``(weapon, mastery)`` pairs.

	Balanced on purpose: half the drills reach far (Ranged or Thrown), half
	are close work, so a hero is never left with six ways to hit an enemy
	they cannot reach. Candidates are ordered by what the hero already
	carries, then filled from what their Guild trained them to hold.

	Each pick is stamped on the Character as a ``Mastery_Of_…`` Tag, so the
	loadout can arm them with the weapons they trained on.
	"""
	existing = list(
			getattr(
					char,
					"weapon_mastery_picks",
					None,
					) or []
			)
	already = {
			weapon
			for weapon, _mastery in existing
			}
	pool = [
			weapon
			for weapon in mastery_candidates(
					char
					)
			if weapon not in already
			]

	far = [
			weapon
			for weapon in pool
			if _reaches_far(
					weapon
					)
			]
	near = [
			weapon
			for weapon in pool
			if not _reaches_far(
					weapon
					)
			]

	# Melee-only Guilds still get the balance they are allowed: their
	# "far" half can only be filled by Thrown weapons.
	want_far = n // 2
	have_far = sum(
			1
			for weapon, _m in existing
			if _reaches_far(
					weapon
					)
			)

	while len(
			existing
			) < n and (
			far or near
			):
		short_on_far = (
			have_far < want_far
			and far
			)
		source = far if short_on_far else (near or far)
		if not source:
			break

		weapon = source.pop(0)
		if _reaches_far(
				weapon
				):
			have_far += 1
		existing.append(
				(
						weapon,
						WEAPON_MASTERIES[weapon],
						)
				)

	char.weapon_mastery_picks = existing

	# Stamp the Tags — this is what lets the loadout arm the hero.
	for weapon, _mastery in existing:
		tag = _mastery_tag(
				weapon
				)
		if char not in tag:
			try:
				tag(
						char
						)
			except Exception:
				pass

	if n:
		return list(
				existing[:n]
				)
	return list(
			existing
			)


def plan_masteries(
		char: Any,
		) -> list[tuple[str, str]]:
	"""Decide this Character's drills from their Guild and level."""
	count = mastery_count(
			char
			)
	if count <= 0:
		return []
	return pick_weapon_masteries(
			char,
			count,
			)


def weapon_mastery_chip(
		char: Any,
		n: int | None = None,
		) -> str:
	"""Left-rail chip value: the weapons this Character drilled."""
	count = mastery_count(
			char
			) if n is None else n
	picks = pick_weapon_masteries(
			char,
			count,
			)
	if not picks:
		return str(
				count
				) if count else "—"
	return ", ".join(
			weapon
			for weapon, _mastery in picks
			)


def weapon_mastery_entry(
		char: Any,
		n: int | None = None,
		) -> str:
	"""Sheet prose naming the chosen weapons and their mastery properties."""
	count = mastery_count(
			char
			) if n is None else n
	picks = pick_weapon_masteries(
			char,
			count,
			)
	if not picks:
		return (
			"*You feel comfortable with the weapons you trained with.*\n\n"
			"Your training with weapons allows you to use the mastery "
			"properties of weapons you practice with."
			)
	if len(
			picks
			) == 1:
		weapons = picks[0][0]
	elif len(
			picks
			) == 2:
		weapons = f"{picks[0][0]} and {picks[1][0]}"
	else:
		weapons = (
			", ".join(
					weapon
					for weapon, _m in picks[:-1]
					)
			+ f", and {picks[-1][0]}"
			)
	parts = [
			"*You feel comfortable with the weapons you trained with.*\n\n"
			"Your training with weapons allows you to use the mastery "
			f"properties of <b>{weapons}</b>. Whenever you finish a Long Rest, "
			"you can change one of those weapon choices.",
			]
	for weapon, mastery in picks:
		blurb = mastery_blurb(
				mastery,
				char,
				)
		header = f"<b>{weapon} Mastery: {mastery}</b>"
		if blurb:
			parts.append(
					f"<br>{header}<br>{blurb}"
					)
		else:
			parts.append(
					f"<br>{header}"
					)
	return "".join(
			parts
			)
