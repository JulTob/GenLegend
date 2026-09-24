"""
Draconic Resilience — the dragon-scale Armor Class of a Draconic Sorcerer.

Thought pattern (read this before the code)
	1. 2024 rule (Sorcerer, Draconic Sorcery, level 3): parts of the body are
	   covered by dragon-like scales. While the Character wears no armor, its
	   base Armor Class equals 10 + Dexterity modifier + Charisma modifier.
	   (The same feature also raises hit points; that stays with the
	   Training Tag that describes it.)
	2. It is its own Tag, independent of Unarmored Defense (Julio,
	   2026-09-24): "Draconic Resilience doesn't exclude Unarmored Defense,
	   so it should be an independent tag. A feature of draconic ancestry."
	   A Character may carry both.
	3. When several no-armour formulas apply, the Character uses the best
	   one. The gear rules take that maximum
	   (``Map_of_Gear_Proficiency.unarmoured_formula``); this module only
	   states its own formula.
	4. The rule says nothing about Shields, so a Shield is allowed.
	5. Reading is pure (Decree 0009, point 7).

Public surface
	Draconic_Resilience(char)     — the Tag
	Draconic_Armour_Class(char)   — 10 + DEX + CHA, or None without the Tag
"""

from __future__ import annotations

from TopKit import Tag

from AtlasActorLudi.Map_of_Scores import Ability_Modifier
from AtlasVenustas import Chip


class Draconic_Resilience( Tag ):
	"""Dragon scales: with no armour on, AC is 10 + Dexterity + Charisma."""

	NAME = "Draconic Resilience"


def Draconic_Armour_Class(
		char,
		) -> int | None:
	"""The scaled Armor Class, or None when the Character has no scales."""
	if char not in Draconic_Resilience:
		return None
	dexterity = Ability_Modifier(
			char,
			"DEX",
			)
	charisma = Ability_Modifier(
			char,
			"CHA",
			)
	return 10 + dexterity + charisma


Draconic_Resilience.CHIPS = (
		Chip(
				"🐉",
				"Scaled AC",
				Draconic_Armour_Class,
				),
		)
	#-- Set after the class, because the Chip's value is the reader above.


__all__ = (
		"Draconic_Armour_Class",
		"Draconic_Resilience",
		)


# ---------------------------------------------------------------------------
# Self-test:  python -m AtlasLusoris.AtlasOfFeatures.Draconic_Resilience
# ---------------------------------------------------------------------------

def _self_test() -> None:

	class Scores:
		DEX = 14
		CHA = 18

	class Dummy:
		def __init__(
				self,
				):
			self.AS = Scores()

	plain = Dummy()
	assert plain not in Draconic_Resilience
	assert Draconic_Armour_Class( plain ) is None

	sorcerer = Dummy()
	Draconic_Resilience( sorcerer )
	assert Draconic_Armour_Class( sorcerer ) == 16

	#-- Independent of Unarmored Defense: both may be carried at once.
	from AtlasLusoris.AtlasOfFeatures.Unarmored_Defense import (
			Unarmored_Defense,
			)
	Unarmored_Defense(
			sorcerer,
			ability="CON",
			shield_allowed=True,
			)
	assert sorcerer in Draconic_Resilience
	assert sorcerer in Unarmored_Defense

	print( "Draconic_Resilience: all checks passed." )


if __name__ == "__main__":
	_self_test()
