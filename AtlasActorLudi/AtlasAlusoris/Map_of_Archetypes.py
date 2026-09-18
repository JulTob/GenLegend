"""Decode former Archetype names into Guild or Background compatibility axes."""
#-- Recovered from the 2026-08-29 bytecode (QST-0134).  The module docstring,
#-- both class docstrings, all five function docstrings, the forty-two legacy
#-- names, the thirty-two AC contributions and the failure message are the
#-- original's, word for word; the transcription was proved instruction for
#-- instruction against the vaulted .pyc before this layout was applied.
#--
#-- Does this module own a domain axis (QST-0134)?  It names two — and neither
#-- is its own.  Guild lives in GuildKit, Background in BackgroundKit, and
#-- Identity_Axis is not a property a Character carries: it is a label for
#-- *which registry a retired name came from*.  An Archetype was the single
#-- mixed identity those two axes replaced, so this file exists to take a name
#-- from the old world and say which of the two new ones owns it.  Giving it a
#-- Tag would put the mixed identity back.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from AtlasLusoris.BackgroundKit import (
		BACKGROUNDS,
		NONPLAYER_ONLY_BACKGROUND_NAMES,
		)
from AtlasLusoris.GuildKit import GUILDS


LEGACY_ARCHETYPE_NAMES = (
		"Artist",
		"Bandit",
		"Barbarian",
		"Bard",
		"Berserker",
		"Charlatan",
		"Cleric",
		"Commoner",
		"Crafter",
		"Criminal",
		"Cultist",
		"Druid",
		"Expert",
		"Explorer",
		"Fighter",
		"Guardian",
		"Healer",
		"Hero",
		"Hunter",
		"Knight",
		"Mage",
		"Mentor",
		"Merchant",
		"Monk",
		"Ninja",
		"Noble",
		"Paladin",
		"Pirate",
		"Priest",
		"Ranger",
		"Rogue",
		"Scholar",
		"Shaman",
		"Soldier",
		"Sorcerer",
		"Spy",
		"Trickster",
		"Traveler",
		"Warlock",
		"Warrior",
		"Witch",
		"Wizard",
		)
	#-- Every name the single mixed identity could take, before it was split.


def Names_Known_To(
		registry,
		) -> tuple[str, ...]:
	"""The legacy names a registry still answers to, in the legacy order."""
	return tuple(
			name
			for name in LEGACY_ARCHETYPE_NAMES
			if name in registry
			)


LEGACY_GUILD_NAMES = Names_Known_To(GUILDS)
	#-- Legacy names a Guild claims: Barbarian, Bard, Cleric, …

LEGACY_BACKGROUND_NAMES = Names_Known_To(BACKGROUNDS)
	#-- Legacy names a Background claims: Artist, Charlatan, Criminal, …

LEGACY_PROFILE_NAMES = Names_Known_To(NONPLAYER_ONLY_BACKGROUND_NAMES)
	#-- The subset of those Backgrounds no Player may be built from.

Archetypes = list(
		LEGACY_ARCHETYPE_NAMES
		)
	#-- The same names as a list, for callers that still expect one.


class Identity_Axis(str, Enum):
	"""Independent Character identity axes used by the compatibility route."""

	GUILD = "guild"
	BACKGROUND = "background"


@dataclass(
		frozen=True,
		slots=True,
		)
class Legacy_Identity:
	"""One former Archetype name routed to its canonical axis."""

	axis: Identity_Axis
	name: str


def Identity_Names(
		character,
		) -> tuple[str, ...]:
	"""Return canonical Guild and Background names once each."""
	result = []

	for attribute in (
			"char_class",
			"background",
			):
		value = getattr(
				character,
				attribute,
				None,
				)

		if not isinstance(
				value,
				str,
				):
			continue
		if not value:
			continue
		if value not in result:
			result.append(
					value
					)

	return tuple(
			result
			)


def Identity_Text(
		character,
		) -> str:
	"""Return the canonical identity view expected by transitional Maps."""
	return " ".join(
			Identity_Names(
					character
					)
			)


def Classify_Archetype(
		name: str,
		) -> Legacy_Identity:
	"""Route an exact legacy name without inventing semantic aliases."""
	#-- Exact, on purpose.  A near-miss is a caller's mistake, and guessing
	#-- which axis was meant would silently build the wrong Character.
	if name in GUILDS:
		return Legacy_Identity(
				Identity_Axis.GUILD,
				name,
				)

	if name in BACKGROUNDS:
		return Legacy_Identity(
				Identity_Axis.BACKGROUND,
				name,
				)

	raise ValueError(
			f"Unknown legacy NonPlayer Archetype: {name!r}."
			)


def Archetype(
		character,
		*,
		dice=None,
		) -> str:
	"""Select a compatibility Archetype through the Character."""
	return character.Pick(
			LEGACY_ARCHETYPE_NAMES,
			dice=dice,
			)


def _identity_modifiers(
		*,
		STR: int = 0,
		DEX: int = 0,
		CON: int = 0,
		INT: int = 0,
		WIS: int = 0,
		CHA: int = 0,
		) -> dict[str, int]:
	"""What each legacy identity used to add to Armour Class, by ability."""
	#-- A retired table, kept because saved NonPlayers were built with it.
	#-- Nothing new should read from here: Armour Class is GearKit's to derive.
	return {
			"Barbarian": CON,
			"Berserker": CON + STR,
			"Charlatan": CHA,
			"Cleric": WIS,
			"Crafter": INT,
			"Criminal": INT,
			"Cultist": WIS,
			"Druid": WIS + CON,
			"Expert": INT + WIS + CHA,
			"Explorer": WIS,
			"Fighter": DEX + STR,
			"Guardian": STR,
			"Hero": STR,
			"Hunter": DEX,
			"Knight": STR + CON,
			"Mage": INT,
			"Monk": DEX + WIS,
			"Ninja": DEX + INT,
			"Noble": DEX,
			"Paladin": STR + CHA,
			"Pirate": DEX,
			"Priest": WIS,
			"Ranger": WIS,
			"Rogue": DEX,
			"Shaman": WIS,
			"Soldier": STR,
			"Sorcerer": CHA,
			"Spy": DEX,
			"Warlock": CHA,
			"Warrior": STR,
			"Witch": WIS,
			"Wizard": INT,
			}


def AC_Identity_modifier(
		name: str | None,
		**abilities: int,
		) -> int:
	"""Return one identity's legacy AC contribution."""
	if not name:
		return 0

	return _identity_modifiers(
			**abilities
			).get(
			name,
			0,
			)


def AC_Archetype_modifier(
		archetype: str = "",
		**abilities: int,
		) -> int:
	"""Compatibility name for callers that still have one mixed identity."""
	return AC_Identity_modifier(
			archetype,
			**abilities,
			)


def AS_Archetype_modifier(
		npc,
		):
	"""Retired compatibility hook; canonical axes now own score influences."""
	return npc


__all__ = (
		"AC_Archetype_modifier",
		"AC_Identity_modifier",
		"AS_Archetype_modifier",
		"Archetype",
		"Archetypes",
		"Classify_Archetype",
		"Identity_Axis",
		"LEGACY_ARCHETYPE_NAMES",
		"LEGACY_BACKGROUND_NAMES",
		"LEGACY_GUILD_NAMES",
		"LEGACY_PROFILE_NAMES",
		"Legacy_Identity",
		)


def _test_the_legacy_names_split_cleanly() -> None:
	"""Every retired name belongs to one axis, or to neither — never to both."""
	both = set(LEGACY_GUILD_NAMES) & set(LEGACY_BACKGROUND_NAMES)
	assert not both, \
			f"A retired name cannot sit on both axes: {sorted(both)}"

	assert set(LEGACY_PROFILE_NAMES) <= set(LEGACY_BACKGROUND_NAMES), \
			"A NonPlayer-only profile is still a Background."

	for name in LEGACY_ARCHETYPE_NAMES:
		assert LEGACY_ARCHETYPE_NAMES.count(name) == 1, \
				f"{name!r} is listed twice."

	#-- The order of each list follows the legacy list, not the registry's.
	assert list(LEGACY_GUILD_NAMES) == [
			name for name in LEGACY_ARCHETYPE_NAMES
			if name in LEGACY_GUILD_NAMES
			], "The Guild names keep the legacy order."


def _test_classification() -> None:
	"""A retired name is routed by which registry still answers to it."""
	for name in LEGACY_GUILD_NAMES:
		routed = Classify_Archetype(name)
		assert routed.axis is Identity_Axis.GUILD, f"{name} is a Guild."
		assert routed.name == name, "Routing does not rename."

	for name in LEGACY_BACKGROUND_NAMES:
		routed = Classify_Archetype(name)
		assert routed.axis is Identity_Axis.BACKGROUND, f"{name} is a Background."

	#-- Exact matching: a near-miss is refused rather than guessed at.
	for unknown in ("Fighterr", "fighter", "", "Adventurer"):
		try:
			Classify_Archetype(unknown)
		except ValueError as refusal:
			assert "Unknown legacy NonPlayer Archetype" in str(refusal), \
					f"{unknown!r} was refused, but not by name: {refusal}"
		else:
			raise AssertionError(
					f"{unknown!r} is not a legacy Archetype and should be refused."
					)


def _test_identity_view() -> None:
	"""The transitional view names each axis once, in a fixed order."""
	from types import SimpleNamespace

	both = SimpleNamespace(char_class="Rogue", background="Criminal")
	assert Identity_Names(both) == ("Rogue", "Criminal"), "Guild first, then Background."
	assert Identity_Text(both) == "Rogue Criminal"

	#-- A Character whose two axes happen to share a name says it once.
	twinned = SimpleNamespace(char_class="Bard", background="Bard")
	assert Identity_Names(twinned) == ("Bard",), "One name, said once."

	#-- Anything missing, blank or not text is simply not named.
	for empty in (
			SimpleNamespace(),
			SimpleNamespace(char_class="", background=""),
			SimpleNamespace(char_class=None, background=None),
			SimpleNamespace(char_class=7, background=["Sage"]),
			):
		assert Identity_Names(empty) == (), f"{empty} names no identity."
		assert Identity_Text(empty) == ""


def _test_the_retired_armour_table() -> None:
	"""The retired AC table still answers as the saved NonPlayers were built."""
	assert AC_Identity_modifier("Barbarian", CON=3) == 3
	assert AC_Identity_modifier("Berserker", CON=3, STR=2) == 5
	assert AC_Identity_modifier("Expert", INT=1, WIS=2, CHA=3) == 6
	assert AC_Identity_modifier("Wizard", INT=4) == 4

	#-- A name the table does not know, and no name at all, both add nothing.
	assert AC_Identity_modifier("Bard", CHA=5) == 0, "Bard was never in the table."
	assert AC_Identity_modifier(None, STR=9) == 0
	assert AC_Identity_modifier("", STR=9) == 0

	#-- The older, mixed-identity spelling is the same rite under another name.
	assert AC_Archetype_modifier("Knight", STR=2, CON=1) == 3
	assert AC_Archetype_modifier() == 0

	#-- The score hook is retired: it hands the NonPlayer back untouched.
	npc = object()
	assert AS_Archetype_modifier(npc) is npc, "A retired hook changes nothing."


def _self_test() -> None:
	_test_the_legacy_names_split_cleanly()
	_test_classification()
	_test_identity_view()
	_test_the_retired_armour_table()
	print("OK — Alusoris Map_of_Archetypes self-test")


if __name__ == "__main__":
	_self_test()
